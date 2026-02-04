from flask import Flask, jsonify, request, send_from_directory
import os
import boto3
import json
import sys
from flask_cors import CORS  # You'll need to install flask-cors
# import pyautogui
import subprocess
import platform
from datetime import datetime, timedelta, timezone
import numpy as np
import requests
import sounddevice as sd  # Used in AudioRecorderThread
import soundfile as sf    # Used in AudioRecorderThread
from PyQt5.QtCore import QDateTime  # For consistent date formatting
import random
from dotenv import load_dotenv

load_dotenv(override=True)
# Fix path to import from sibling directory
print("USERNAME from env:", os.getenv("USERNAME"))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Path being added to sys.path:", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Current sys.path:", sys.path)
try:
    # Try importing from server directory (sibling to window directory)
    from server.aws import S3
    print("Successfully imported S3 from server.aws")
except ImportError as e:
    print(f"Error importing modules: {e}")
    # Create a minimal S3 stub so the app can still run
    class S3:
        def __init__(self):
            self.client = boto3.client('s3', region_name='us-west-2')
            self.bucket_name = "digital-diary"

        def get(self):
            return self

        def get_presigned_url(self, file_path):
            object_name = f"sophia/{os.path.basename(file_path)}"
            url = self.client.generate_presigned_url(
                'put_object',
                Params={'Bucket': self.bucket_name, 'Key': object_name},
                ExpiresIn=3600
            )
            return url
# Fix issue where sys.stdin, sys.stdout, or sys.stderr is None in PyInstaller
if sys.stdin is None:
    sys.stdin = open(os.devnull)
if sys.stdout is None:
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    sys.stdout = open(os.path.join(log_dir, 'app.log'), 'w')
if sys.stderr is None:
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    sys.stderr = open(os.path.join(log_dir, 'error.log'), 'w')

# Add a function to log to both console and file
def log_message(message):
    print(message)
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, 'app.log'), 'a') as f:
        f.write(f"{message}\n")

# Use the log_message function for important debug info
log_message("Path being added to sys.path: " + str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
log_message("Current sys.path: " + str(sys.path))

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React app to communicate with Flask

# S3 Setup
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
USERNAME = os.getenv("USERNAME")
s3_client = boto3.client('s3', region_name=AWS_REGION)

# Get the base directory (similar to how overlay.py gets to "recordings")
# This ensures we save to the project's root recordings directory
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECORDINGS_DIR = os.path.join(base_dir, "recordings")
SCREENSHOTS_DIR = os.path.join(base_dir, "screenshots")
AUDIO_DIR = os.path.join(base_dir, "audio")
THUMBNAILS_DIR = os.path.join(RECORDINGS_DIR, "thumbnails")

# Figure out OS and architecture for ffmpeg binary path
BIN_DIR = os.path.join(base_dir, "bin")
platform_machine = platform.machine().lower()
if platform_machine in ['x86_64', 'amd64']:
    platform_arch = 'x64'
elif platform_machine in ['aarch64', 'arm64']:
    platform_arch = 'arm64'
else:
    platform_arch = 'unknown'
platform_os = platform.system().lower()
if platform_os == 'darwin':
    platform_os = 'mac'
elif platform_os == 'windows':
    platform_os = 'win'
FFMPEG_PATH = os.path.join(
    BIN_DIR,
    platform_os,
    platform_arch,
    'ffmpeg' + ('.exe' if platform_os == 'win' else '')
)


# Create directories (same as in overlay.py)
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(THUMBNAILS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Global variables for recording state
recorder_thread = None
audio_recorder = None

ffmpeg = None
ffmpeg_output = None

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "API is working!"})

@app.route('/api/media_aws', methods=['GET'])
def get_media_aws():
    try:
        # List objects in the user's directory in S3
        prefix = f"{USERNAME}/"
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=prefix
        )

        if 'Contents' not in response:
            return jsonify([])

        media_list = []
        for idx, item in enumerate(response['Contents'], 1):
            # Extract filename and extension
            filename = os.path.basename(item['Key'])
            file_extension = os.path.splitext(filename)[1][1:].lower()

            # Extract username and game_id from S3 path
            # Format: username/game_id/filename
            parts = item['Key'].split('/')
            owner_user_id = parts[0]
            game_id = parts[1] if len(parts) > 2 else None

            # Determine media type
            media_type = "unknown"
            if file_extension in ['mp4', 'mov']:
                media_type = "video"
            elif file_extension in ['mp3', 'wav']:
                media_type = "audio"
            elif file_extension in ['jpg', 'jpeg', 'png']:
                media_type = "screenshot"

            # Generate presigned URL
            media_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET_NAME, 'Key': item['Key']},
                ExpiresIn=3600
            )

            # Transform into media data type format
            media_item = {
                "media_id": idx,
                "type": media_type,
                "media_url": media_url,
                "timestamp": item['LastModified'].isoformat(),
                "owner_user_id": owner_user_id,
                "game_id": game_id,
                "game": game_id if game_id else "game1"  # Use game_id if available, else fallback
            }

            media_list.append(media_item)

        # Apply filters if provided
        media_type = request.args.get('media_type')
        if media_type:
            media_list = [item for item in media_list if item['type'] == media_type]

        return jsonify(media_list)

    except Exception as e:
        print(f"Error in get_media_aws: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-presigned-url', methods=['POST'])
def generate_presigned_url():
    try:
        data = request.json
        file_name = data.get('file_name')
        username = data.get('username')

        if not file_name or not username:
            return jsonify({"error": "Missing file_name or username"}), 400

        object_name = f"{username}/{file_name}"
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )

        return jsonify({"url": url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/latest-screenshot', methods=['GET'])
def latest_screenshot():
    """Returns the URL for the latest screenshot"""
    try:
        prefix = USERNAME + "/screenshot_"
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

        if 'Contents' in response:
            files = [file for file in response['Contents'] if file['Key'].startswith(prefix)]

            if files:
                latest_file = sorted(files, key=lambda x: x['LastModified'], reverse=True)[0]['Key']
                screenshot_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': latest_file},
                    ExpiresIn=3600
                )
                return jsonify({"screenshot_url": screenshot_url})

        return jsonify({"screenshot_url": None})
    except Exception as e:
        print(f"Error in latest_screenshot: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Get the latest screenshot from S3
@app.route('/api/hero-image', methods=['GET'])
def get_hero_image():
    try:
        # Get the latest screenshot from S3
        prefix = USERNAME + "/screenshot_"
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        
        if 'Contents' in response:
            files = [file for file in response['Contents'] if file['Key'].startswith(prefix)]
            
            if files:
                # Sort by LastModified (newest first)
                latest_file = sorted(files, key=lambda x: x['LastModified'], reverse=True)[0]['Key']
                screenshot_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': latest_file},
                    ExpiresIn=3600
                )
                return jsonify({"hero_image_url": screenshot_url})
        
        # If no screenshots found, return a default image URL or null
        return jsonify({"hero_image_url": None})
    except Exception as e:
        print(f"Error in get_hero_image: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/random-screenshot-by-days/<int:days>', methods=['GET'])
def get_random_screenshot_by_days(days):
    """Returns the URL for a randomly selected screenshot taken approximately X days ago or longer"""
    try:
        # Calculate the date from approximately X days ago
        # Make sure to use timezone-aware datetime
        target_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # For exact date matching (commented out for now)
        # Extract just the date part (year, month, day) for comparison
        # target_date_only = target_date.date()
        
        prefix = USERNAME + "/screenshot_"
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        
        if 'Contents' in response:
            print(f"Found content in S3 bucket")
            # Filter files to only include those from X days ago or longer
            files = [file for file in response['Contents'] 
                    if file['Key'].startswith(prefix) and 
                    file['LastModified'] <= target_date]
            
            # For exact date matching (commented out for now)
            # files = [file for file in response['Contents'] 
            #         if file['Key'].startswith(prefix) and 
            #         file['LastModified'].date() == target_date_only]
            
            print(f"Found {len(files)} screenshots from {days} days ago or older")
            if files:
                # Randomly select one file from the filtered list
                random_file = random.choice(files)['Key']
                screenshot_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': random_file},
                    ExpiresIn=3600
                )
                return jsonify({"screenshot_url": screenshot_url})
        
        return jsonify({"screenshot_url": None})
    except Exception as e:
        print(f"Error in get_random_screenshot_by_days: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/screenshots/<filename>')
def get_screenshot(filename):
    """Serves the screenshot file."""
    return send_from_directory(SCREENSHOTS_DIR, filename)

@app.route('/api/screenshot', methods=['POST'])
def upload_screenshot():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ['png', 'jpg', 'jpeg']:
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Generate presigned URL for upload
        object_name = f"{USERNAME}/{file.filename}"
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )

        # Upload to S3
        response = requests.put(url, data=file)
        if response.status_code != 200:
            raise Exception("Failed to upload screenshot")
        else:
            return jsonify({
                'status': 'success',
                'url': url
            })
    except Exception as e:
        print(f'Screenshot error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/start', methods=['POST'])
def start_screen_recording():
    try:
        global ffmpeg
        global ffmpeg_output

        url = 'srt://127.0.0.1:40052'  # Use 127.0.0.1 to listen on localhost

        if (ffmpeg):
            if ffmpeg.poll() is None:
                return jsonify({'status': 'ffmpeg available', 'url': url}), 200
            else:
                ffmpeg = None  # Reset if process has ended

        timestamp = datetime.now().strftime('recording_%Y%m%d_%H%M%S.mkv')
        ffmpeg_output = os.path.normpath(os.path.join(RECORDINGS_DIR, timestamp))
        
        log_message(f"Output file path: {ffmpeg_output}")
        log_message(f"FFmpeg path: {FFMPEG_PATH}")
        log_message(f"FFmpeg exists: {os.path.exists(FFMPEG_PATH)}")
        
        # Start FFmpeg process - COPY BOTH video AND audio
        ffmpeg = subprocess.Popen(
            [FFMPEG_PATH, 
             '-probesize', '10M',
             '-flags', 'low_delay',
             '-i', url + '?mode=listener',
             '-map', '0:v',   # Map video first
             '-map', '0:a?',   # Map audio second
             '-c:v', 'copy',  # Then specify video codec
             '-c:a', 'copy',  # Then specify audio codec
             ffmpeg_output],
            stdin=subprocess.PIPE
        )

        log_message(f"Started ffmpeg with PID {ffmpeg.pid} for screen recording.")
        
        # Check if process started successfully
        try:
            ffmpeg.wait(timeout=0.5)
            # Process ended immediately - something went wrong
            ffmpeg = None
            return jsonify({'error': f'FFmpeg failed to start'}), 500
        except subprocess.TimeoutExpired:
            # Process is still running - good!
            log_message("FFmpeg process is running")

        return jsonify({'status': 'ffmpeg available', 'url': url + '?mode=caller'}), 200
        
    except Exception as e:
        log_message(f"Recording start error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/status', methods=['GET'])
def recording_status():
    try:
        global ffmpeg
        if ffmpeg and ffmpeg.poll() is None:
            return jsonify({'recording': True}), 200
        else:
            return jsonify({'recording': False}), 200
    except Exception as e:
        print(f"Recording status error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/stop', methods=['POST'])
def stop_screen_recording():
    try:
        global ffmpeg
        global ffmpeg_output

        # Check if recording is in progress
        if not ffmpeg:
            return jsonify({'error': 'No active recording'}), 400

        # Send 'q' to FFmpeg stdin to gracefully stop (recommended method)
        try:
            ffmpeg.communicate(input=b'q', timeout=5)
            log_message("Sent 'q' to ffmpeg stdin to stop recording.")
        except:
            log_message("Failed to send 'q' to ffmpeg stdin, attempting to terminate.")
            ffmpeg.terminate()
        
        ffmpeg = None
        log_message("Stopped ffmpeg for screen recording.")

        video_url = None

        # Upload the recording to S3
        try:
            object_name = f"{USERNAME}/recordings/{os.path.basename(ffmpeg_output)}"
            url = s3_client.generate_presigned_url(
                'put_object',
                Params={'Bucket': BUCKET_NAME, 'Key': object_name},
                ExpiresIn=3600
            )
            with open(ffmpeg_output, 'rb') as f:
                response = requests.put(url, data=f)
                if response.status_code != 200:
                    raise Exception("Failed to upload recording")
            video_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET_NAME, 'Key': object_name},
                ExpiresIn=3600
            )
            log_message("Recording uploaded successfully.")
        except Exception as e:
            log_message(f"Error uploading recording: {e}")
            return jsonify({'error': f"Failed to upload recording: {str(e)}"}), 500

        # Return paths
        return jsonify({
            'status': 'stopped',
            'video_url': video_url,
            'thumbnail_path': "not implemented"
        })
    except Exception as e:
        print(f"Recording stop error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/start', methods=['POST'])
def start_audio_recording():
    try:
        global audio_recorder

        # Initialize audio recorder with the same parameters as AudioRecorderThread
        audio_recorder = {
            'recording': True,
            'frames': [],
            'samplerate': 44100
        }

        # Detect the default input device
        default_device = sd.query_devices(kind='input')

        # Ensure the device supports at least 1 channel (same logic as AudioRecorderThread)
        channels = min(default_device['max_input_channels'], 2)
        if channels < 1:
            return jsonify({'error': "No valid input channels found on the default recording device."}), 500

        audio_recorder['channels'] = channels

        def audio_callback(indata, frames, time, status):
            if status:
                print(status)
            audio_recorder['frames'].append(indata.copy())

        # Start recording in a separate thread
        def record_audio():
            try:
                with sd.InputStream(samplerate=audio_recorder['samplerate'],
                                   channels=audio_recorder['channels'],
                                   callback=audio_callback):
                    while audio_recorder['recording']:
                        sd.sleep(100)  # Sleep to allow audio recording to happen
            except Exception as e:
                print(f"Error during audio recording: {e}")

        import threading
        recording_thread = threading.Thread(target=record_audio)
        recording_thread.daemon = True  # Make thread daemon so it exits when main thread exits
        recording_thread.start()

        return jsonify({'status': 'started'})
    except Exception as e:
        print(f"Audio start error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/stop', methods=['POST'])
def stop_audio_recording():
    try:
        global audio_recorder
        if audio_recorder and audio_recorder['recording']:
            # Stop recording
            audio_recorder['recording'] = False

            # Wait a bit for the recording to finalize
            sd.sleep(200)

            # Generate filename using QDateTime for consistency
            now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
            audio_path = os.path.join(AUDIO_DIR, f'audio_recording_{now}.wav')

            try:
                # Save the audio data to a file (same as AudioRecorderThread)
                sf.write(audio_path, np.concatenate(audio_recorder['frames']), audio_recorder['samplerate'])
                print(f"Audio recording finalized at {audio_path}")
            except Exception as e:
                print(f"Error saving audio file: {e}")
                return jsonify({'error': f"Failed to save audio: {str(e)}"}), 500

            # Upload to S3
            try:
                object_name = f"{USERNAME}/{os.path.basename(audio_path)}"
                url = s3_client.generate_presigned_url(
                    'put_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': object_name},
                    ExpiresIn=3600
                )

                with open(audio_path, 'rb') as f:
                    response = requests.put(url, data=f)
                    if response.status_code != 200:
                        raise Exception("Failed to upload audio file")
                print("Audio uploaded successfully.")
            except Exception as e:
                print(f"Error uploading audio: {e}")
                return jsonify({'error': f"Failed to upload audio: {str(e)}"}), 500

            # Clear the recorder
            temp_path = audio_path  # Save path before clearing
            audio_recorder = None

            return jsonify({
                'status': 'stopped',
                'path': temp_path
            })

        return jsonify({'error': 'No active recording'}), 400
    except Exception as e:
        print(f"Audio stop error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/media', methods=['GET'])
def get_media():
    try:
        media_type = request.args.get('media_type')
        user_id = request.args.get('user_id')

        MEDIA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/media.json'))

        with open(MEDIA_FOLDER, 'r') as file:
            data = json.load(file)

        media = data['media']

        if media_type:
            media = [item for item in media if item['type'] == media_type]

        if user_id:
            media = [item for item in media if str(item['owner_user_id']) == str(user_id)]

        return jsonify(media)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/update', methods=['POST'])
def update_session():
    try:
        data = request.json
        game_id = data.get('game_id')
        
        if not game_id:
            return jsonify({"error": "game_id is required"}), 400
        
        # Import aws.py's S3 class and call update_session
        from server.aws import S3
        s3 = S3()
        success = s3.update_session(game_id)
        
        if not success:
            return jsonify({"error": "Failed to update session in S3"}), 500
        
        return jsonify({
            "status": "success",
            "game_id": game_id
        })
        
    except Exception as e:
        print(f"Error updating session: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/latest', methods=['GET'])
def get_latest_session():
    try:
        # Import aws.py's S3 class and call get_latest_session
        from server.aws import S3
        s3 = S3()
        latest_session = s3.get_latest_session()
        
        if not latest_session:
            return jsonify({
                "game_id": None,
                "timestamp": None
            })
        
        return jsonify(latest_session)
        
    except Exception as e:
        print(f"Error getting latest session: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        # Get the path to user.json
        user_json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'user.json')

        # Read the JSON file
        with open(user_json_path, 'r') as f:
            user_data = json.load(f)

        return jsonify(user_data['users'])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')