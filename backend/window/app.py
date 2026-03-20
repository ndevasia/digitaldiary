from flask import Flask, jsonify, request, send_from_directory, render_template
import os
import boto3
import json
import sys
import signal
from flask_cors import CORS  # You'll need to install flask-cors
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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    # Try importing from server directory (sibling to window directory)
    from server.aws import S3
    print("Successfully imported S3 from server.aws")
except ImportError as e:
    print(f"Error importing modules: {e}")
    # Create a minimal S3 stub so the app can still run
    class S3:
        def __init__(self, username=None):
            self.client = boto3.client('s3', region_name='us-west-2')
            self.bucket_name = "digital-diary"
            self.username = username

        def get(self):
            return self

        def get_presigned_url(self, file_path):
            object_name = f"{os.path.basename(file_path)}"
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


def get_default_username():
    """Get the default username (user 0) from user.json"""
    try:
        user_json_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'model', 'user.json'
        )
        
        if os.path.exists(user_json_path):
            with open(user_json_path, 'r') as f:
                data = json.load(f)
            users = data.get('users', [])
            # Find user with user_id = 0
            for user in users:
                if user.get('user_id') == 0:
                    return user.get('username')
        
        # Fallback if no user 0 found
        return os.getenv('USERNAME', 'User')
    except Exception as e:
        log_message(f"Error getting default username: {e}")
        return os.getenv('USERNAME', 'User')

def get_user_id_from_username(username):
    """Get the user_id from a username by looking it up in user.json"""
    try:
        ensure_user_json_exists()
        user_json_path = get_user_json_path()
        
        with open(user_json_path, 'r') as f:
            user_data = json.load(f)
        
        users = user_data.get('users', [])
        for user in users:
            if user.get('username') == username:
                return user.get('user_id')
        
        return None
    except Exception as e:
        print(f"Error getting user_id from username: {e}")
        return None

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React app to communicate with Flask


# Helper functions for user.json
def get_user_json_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'user.json')

def ensure_user_json_exists():
    """Ensure user.json exists with a basic structure."""
    try:
        path = get_user_json_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(path):
            # Create default owner with user_id 0 (ideally we will never hit this branch of logic)
            default_user = {"user_id": 0, "username": "owner"}
            tmp_path = path + '.tmp'
            with open(tmp_path, 'w') as f:
                json.dump({"users": [default_user]}, f, indent=4)
            os.replace(tmp_path, path)
    except Exception as e:
        print(f"Error ensuring user.json exists: {str(e)}")

# S3 Setup
AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
s3_client = boto3.client('s3', region_name=AWS_REGION)

# Get the base directory (similar to how overlay.py gets to "recordings")
# This ensures we save to the project's root recordings directory
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECORDINGS_DIR = os.path.join(base_dir, "recordings")
SCREENSHOTS_DIR = os.path.join(base_dir, "screenshots")
AUDIO_DIR = os.path.join(base_dir, "audio")
THUMBNAILS_DIR = os.path.join(RECORDINGS_DIR, "thumbnails")
PROFILE_PICS_DIR = os.path.join(base_dir, "profile_pics") # Profile picture directory

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
os.makedirs(PROFILE_PICS_DIR, exist_ok=True)

# Global variables for recording state
recorder_thread = None
audio_recorder = None

# recording_processes will map file UIDs
# to processes recording to those files
# to manage multiple recordings and ensure 
# we can stop the correct one on exit
recording_processes = {}

# recording_metadata will store app_name and user_with for each active recording
recording_metadata = {}
# Define a cleanup function to run when the app closes
def graceful_exit(signum, frame):
    print("Received stop signal. Cleaning up...")
    
    # 1. Stop Video Recording if active
    global recorder_thread
    if recorder_thread and hasattr(recorder_thread, 'recording') and recorder_thread.recording:
        print("Stopping active video recording...")
        try:
            recorder_thread.stop()
            # Wait briefly for file to save
            import time
            time.sleep(1)
        except Exception as e:
            print(f"Error stopping video recording: {e}")
        
    # 2. Stop Audio Recording if active
    global audio_recorder
    if audio_recorder and audio_recorder.get('recording', False):
        print("Stopping active audio recording...")
        try:
            # Stop recording
            audio_recorder['recording'] = False
            sd.sleep(200)  # Wait for recording to finalize
            
            # Save the audio file
            if audio_recorder['frames']:
                now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
                audio_path = os.path.join(AUDIO_DIR, f'audio_recording_{now}.wav')
                sf.write(audio_path, np.concatenate(audio_recorder['frames']), audio_recorder['samplerate'])
                print(f"Audio recording saved to {audio_path}")
        except Exception as e:
            print(f"Error stopping audio recording: {e}")
    
    print("Cleanup done. Exiting.")
    sys.exit(0)

# Register the signals
signal.signal(signal.SIGTERM, graceful_exit)  # Handle kill() from Electron
signal.signal(signal.SIGINT, graceful_exit)   # Handle Ctrl+C

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "API is working!"})

@app.route('/api/media_aws', methods=['GET'])
def get_media_aws():
    try:
        username = get_default_username()
        # Support optional single 'username' query param so callers can request another user's media
        req_username = request.args.get('username')
        prefix_username = req_username if req_username else username
        # List objects in the specified user's directory in S3
        prefix = f"{prefix_username}/"
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

        if 'Contents' not in response:
            return jsonify([])

        media_list = []
        for idx, item in enumerate(response['Contents'], 1):
            # Extract filename and extension
            filename = os.path.basename(item['Key'])
            file_extension = os.path.splitext(filename)[1][1:].lower()

            # Extract username and session_id from S3 path
            # Format: username/session_id/filename
            parts = item['Key'].split('/')
            s3_username = parts[0]
            session_id = parts[1] if len(parts) > 2 else None

            # Convert S3 username to integer user_id
            owner_user_id = get_user_id_from_username(s3_username)
            if owner_user_id is None:
                # Fallback: if user not found, skip this item
                print(f"Warning: User '{s3_username}' not found in user.json")
                continue

            # Determine media type
            media_type = "unknown"
            if file_extension in ['mp4', 'mov', 'mkv']:
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

            # Get custom metadata from S3 object tags
            try:
                tag_response = s3_client.get_object_tagging(Bucket=BUCKET_NAME, Key=item['Key'])
                s3_metadata = {tag['Key']: tag['Value'] for tag in tag_response.get('TagSet', [])}
            except Exception as e:
                print(f"Warning: Could not retrieve tags for {item['Key']}: {e}")
                s3_metadata = {}

            # Transform into media data type format
            media_item = {
                "media_id": idx,
                "type": media_type,
                "media_url": media_url,
                "timestamp": item['LastModified'].isoformat(),
                "owner_user_id": owner_user_id,
                "session_id": session_id,
                "app_name": session_id if session_id else "app1",  # Use session_id if available, else fallback
                "s3_key": item['Key']  # Add the actual S3 key for deletion
            }

            # Apply custom metadata from S3 object headers
            # S3 metadata will override the defaults
            media_item.update(s3_metadata)

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
        username = get_default_username()
        # List all objects under USERNAME prefix to find any screenshots
        prefix = username + "/screenshot_"
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)

        if 'Contents' in response:
            # Find all screenshot files (recursively from any session folder)
            screenshot_files = [file for file in response['Contents'] if 'screenshot_' in file['Key']]

            if screenshot_files:
                latest_file = sorted(screenshot_files, key=lambda x: x['LastModified'], reverse=True)[0]['Key']
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
        
        username = get_default_username()
        prefix = username + "/screenshot_"
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
        # Get metadata from form data
        app_name = request.form.get('app_name', '')
        user_with = request.form.get('user_with', '')
        
        # Generate presigned URL for upload
        current_username = get_default_username()
        object_name = f"{current_username}/{file.filename}"
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )

        # Upload to S3
        response = requests.put(url, data=file)
        if response.status_code != 200:
            raise Exception("Failed to upload screenshot")
        
        # Tag the object with metadata
        try:
            s3_client.put_object_tagging(
                Bucket=BUCKET_NAME,
                Key=object_name,
                Tagging={
                    'TagSet': [
                        {'Key': 'app_name', 'Value': app_name},
                        {'Key': 'user_with', 'Value': user_with}
                    ]
                }
            )
        except Exception as e:
            log_message(f"Warning: Could not tag screenshot object: {e}")
        
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
        global recording_processes
        global recording_metadata

        # Extract metadata from request body
        data = request.json or {}
        app_name = data.get('app_name', '')
        user_with = data.get('user_with', '')

        port = random.randint(40000, 50000)
        url = f"srt://127.0.0.1:{port}"

        file_uid = datetime.now().strftime(f"{port}%Y%m%d_%H%M%S")
        filename = f"recording_{file_uid}.mkv"
        ffmpeg_output = os.path.normpath(os.path.join(RECORDINGS_DIR, filename))
        
        log_message(f"Output file path: {ffmpeg_output}")
        log_message(f"FFmpeg path: {FFMPEG_PATH}")
        log_message(f"FFmpeg exists: {os.path.exists(FFMPEG_PATH)}")
        
        # Start FFmpeg process
        ffmpeg_process = subprocess.Popen(
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
        recording_processes[file_uid] = ffmpeg_process
        # Store metadata for this recording
        recording_metadata[file_uid] = {
            'app_name': app_name,
            'user_with': user_with
        }

        log_message(f"Started ffmpeg with PID {ffmpeg_process.pid} for screen recording.")
        
        # Check if process started successfully
        try:
            ffmpeg_process.wait(timeout=0.5)
            # Process ended immediately - something went wrong
            del recording_processes[file_uid]
            del recording_metadata[file_uid]
            return jsonify({'error': f'FFmpeg failed to start'}), 500
        except subprocess.TimeoutExpired:
            # Process is still running - good!
            log_message("FFmpeg process is running")

        return jsonify({'status': 'ffmpeg available', 'url': url + '?mode=caller', 'uid': file_uid}), 200
        
    except Exception as e:
        log_message(f"Recording start error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/status/<file_uid>', methods=['GET'])
def recording_status(file_uid):
    try:
        global recording_processes
        if file_uid in recording_processes and recording_processes[file_uid].poll() is None:
            return jsonify({'recording': True}), 200
        else:
            return jsonify({'recording': False}), 200
    except Exception as e:
        print(f"Recording status error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/stop/<file_uid>', methods=['POST'])
def stop_screen_recording(file_uid):
    try:
        global recording_processes
        global recording_metadata

        # Check if recording is in progress
        if file_uid not in recording_processes:
            return jsonify({'error': 'No active recording'}), 400

        ffmpeg_process = recording_processes[file_uid]

        # Send 'q' to FFmpeg stdin to gracefully stop
        try:
            ffmpeg_process.communicate(input=b'q', timeout=5)
            log_message("Sent 'q' to ffmpeg stdin to stop recording.")
        except:
            log_message("Failed to send 'q' to ffmpeg stdin, attempting to terminate.")
            ffmpeg_process.terminate()
        
        del recording_processes[file_uid]
        log_message("Stopped ffmpeg for screen recording.")

        filename = f"recording_{file_uid}.mkv"
        ffmpeg_output = os.path.normpath(os.path.join(RECORDINGS_DIR, filename))
        video_url = None

        # Upload the recording to S3
        try:
            object_name = f"{get_default_username()}/recordings/{filename}"
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
            
            # Tag the object with metadata
            try:
                metadata = recording_metadata.get(file_uid, {})
                app_name = metadata.get('app_name', '')
                user_with = metadata.get('user_with', '')
                
                s3_client.put_object_tagging(
                    Bucket=BUCKET_NAME,
                    Key=object_name,
                    Tagging={
                        'TagSet': [
                            {'Key': 'app_name', 'Value': app_name},
                            {'Key': 'user_with', 'Value': user_with}
                        ]
                    }
                )
                log_message(f"Tagged recording with app_name={app_name}, user_with={user_with}")
            except Exception as e:
                log_message(f"Warning: Could not tag recording object: {e}")
            
            # Clean up metadata
            if file_uid in recording_metadata:
                del recording_metadata[file_uid]
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

@app.route('/api/audio/upload', methods=['POST'])
def upload_audio_recording():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    file = request.files['file']
    if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in ['mp3', 'wav', 'flac']:
        return jsonify({'error': 'Invalid file type'}), 400
    
    try:
        # Get metadata from form data
        app_name = request.form.get('app_name', '')
        user_with = request.form.get('user_with', '')
        
        # Generate presigned URL for upload
        object_name = f"{get_default_username()}/recordings/{file.filename}"
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )

        # Upload to S3
        response = requests.put(url, data=file)
        if response.status_code != 200:
            raise Exception("Failed to upload audio recording")
        
        # Tag the object with metadata
        try:
            s3_client.put_object_tagging(
                Bucket=BUCKET_NAME,
                Key=object_name,
                Tagging={
                    'TagSet': [
                        {'Key': 'app_name', 'Value': app_name},
                        {'Key': 'user_with', 'Value': user_with}
                    ]
                }
            )
        except Exception as e:
            log_message(f"Warning: Could not tag audio object: {e}")
        
        return jsonify({
            'status': 'success',
            'url': url
        })
    except Exception as e:
        print(f'Audio upload error: {str(e)}')
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
            # Convert user_id to int for consistent filtering with integer user_ids
            try:
                user_id_int = int(user_id)
                media = [item for item in media if item['owner_user_id'] == user_id_int]
            except ValueError:
                # If conversion fails, fall back to string comparison
                media = [item for item in media if str(item['owner_user_id']) == str(user_id)]

        return jsonify(media)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/create', methods=['POST'])
def create_session():
    try:
        data = request.json
        app_name = data.get('appName')
        user_with = data.get('userWith') or ''  # Can be empty string if no friends selected
        
        if not app_name:
            return jsonify({"error": "appName is required"}), 400
        
        # Validate that user_with contains only actual friends
        if user_with:
            try:
                ensure_user_json_exists()
                user_json_path = get_user_json_path()
                with open(user_json_path, 'r') as f:
                    user_data = json.load(f)
                friends = [u.get('username') for u in user_data.get('users', []) if u.get('user_id', 0) > 0]
                
                # Parse plus-separated friends and validate
                provided_friends = [f.strip() for f in user_with.split('+') if f.strip()]
                invalid_friends = [f for f in provided_friends if f not in friends]
                
                if invalid_friends:
                    return jsonify({"error": f"Invalid friends: {'/'.join(invalid_friends)}"}), 400
            except Exception as e:
                log_message(f"Warning: Could not validate friends: {e}")
                # Don't fail the session creation if validation fails, just log it
        
        # Import aws.py's S3 class and call create_session
        from server.aws import S3
        s3 = S3()
        success = s3.create_session(app_name, user_with)
        
        if not success:
            return jsonify({"error": "Failed to create session in S3"}), 500
        
        return jsonify({
            "status": "success",
            "app_name": app_name,
            "user_with": user_with
        })
        
    except Exception as e:
        print(f"Error creating session: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/update', methods=['POST'])
def update_session():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id:
            return jsonify({"error": "session_id is required"}), 400
        
        # Import aws.py's S3 class and call update_session
        from server.aws import S3
        current_username = get_default_username()
        s3 = S3(username=current_username)
        success = s3.update_session(session_id)
        
        if not success:
            return jsonify({"error": "Failed to update session in S3"}), 500
        
        return jsonify({
            "status": "success",
            "session_id": session_id
        })
        
    except Exception as e:
        print(f"Error updating session: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/latest', methods=['GET'])
def get_latest_session():
    try:
        # Import aws.py's S3 class and call get_latest_session
        from server.aws import S3
        current_username = get_default_username()
        s3 = S3(username=current_username)
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

@app.route('/api/session/end', methods=['POST'])
def end_session():
    try:
        # Import aws.py's S3 class and call end_session
        from server.aws import S3
        s3 = S3()
        success = s3.end_session()
        
        if not success:
            return jsonify({"error": "Failed to end session in S3"}), 500
        
        return jsonify({"status": "success"})
        
    except Exception as e:
        print(f"Error ending session: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/sessions/list', methods=['GET'])
def list_sessions():
    try:
        # Import aws.py's S3 class and get all sessions
        from server.aws import S3
        s3 = S3()
        sessions = s3.get_all_sessions()
        
        if not sessions:
            return jsonify([])
        
        return jsonify(sessions)
        
    except Exception as e:
        print(f"Error listing sessions: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/session/delete', methods=['POST'])
def delete_session():
    try:
        data = request.json
        start_timestamp = data.get('start_timestamp')
        
        if not start_timestamp:
            return jsonify({"error": "start_timestamp is required"}), 400
        
        # Import aws.py's S3 class and delete the session
        from server.aws import S3
        s3 = S3()
        success = s3.delete_session(start_timestamp)
        
        if not success:
            return jsonify({"error": "Session not found or could not be deleted"}), 404
        
        return jsonify({"status": "success"})
        
    except Exception as e:
        print(f"Error deleting session: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/media/delete', methods=['DELETE', 'POST'])
def delete_media():
    try:
        # Support both JSON body (for DELETE) and form data (for POST for backwards compatibility)
        if request.method == 'DELETE':
            data = request.get_json() or {}
        else:
            data = request.get_json() or request.form.to_dict()
        
        file_key = data.get('file_key')
        
        if not file_key:
            return jsonify({"error": "file_key is required"}), 400
        
        # Import aws.py's S3 class and delete the file
        from server.aws import S3
        s3 = S3()
        success = s3.delete_file(file_key)
        
        if not success:
            return jsonify({"error": "Failed to delete file from S3"}), 500
        
        return jsonify({"status": "success"})
        
    except Exception as e:
        print(f"Error deleting media: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/media/update-metadata', methods=['POST'])
def update_media_metadata():
    try:
        data = request.json
        s3_key = data.get('s3_key')
        metadata = data.get('metadata', {})
        
        if not s3_key:
            return jsonify({"error": "s3_key is required"}), 400
        
        # Trim whitespace from all metadata values
        trimmed_metadata = {
            key: value.strip() if isinstance(value, str) else value 
            for key, value in metadata.items()
        }
        
        # Import aws.py's S3 class and update metadata
        from server.aws import S3
        s3 = S3()
        success = s3.update_media_metadata(s3_key, trimmed_metadata)
        
        if not success:
            return jsonify({"error": "Failed to update media metadata"}), 500
        
        return jsonify({"status": "success"})
        
    except Exception as e:
        print(f"Error updating media metadata: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        # Ensure user.json exists 
        ensure_user_json_exists()

        # Read the JSON file
        user_json_path = get_user_json_path()
        with open(user_json_path, 'r') as f:
            user_data = json.load(f)

        return jsonify(user_data.get('users', []))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Upload profile picture to directory    
@app.route('/api/upload-profile-pic', methods=['POST'])
def upload_profile_pic():
    try:
        username = get_default_username()
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Simple extension check
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return jsonify({"error": "File type not supported"}), 400
        
        _, ext = os.path.splitext(file.filename) 
        ext = ext.lower()
        object_name = f"{username}/profile{ext}"

        content_types = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif'
        }

        # Ensure pointer is at the start
        file.seek(0)

        # Uploads new profile picture first
        s3_client.upload_fileobj(
            file,
            BUCKET_NAME,
            object_name,
            # octet-stream used for fallback if unknown extension
            ExtraArgs={'ContentType': content_types.get(ext, 'application/octet-stream')}
        )

        # Clean up old/different extensions
        existing_files = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{username}/profile")

        if 'Contents' in existing_files:
        # Filter out the file we JUST uploaded so we don't delete it
            delete_keys = [
                {'Key': obj['Key']} 
                for obj in existing_files['Contents'] 
                if obj['Key'] != object_name
            ]
            if delete_keys:
                s3_client.delete_objects(Bucket=BUCKET_NAME, Delete={'Objects': delete_keys})

        new_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )
        
        return jsonify({"message": "Success", "url": new_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# Retrieve profile picture from directory
@app.route('/api/profile-pic', methods=['GET'])
def get_profile_pic():
    try:
        username = get_default_username()
        # List objects with the prefix for profile pictures
        response = s3_client.list_objects_v2(
            Bucket=BUCKET_NAME, 
            Prefix=f"{username}/profile"
        )

        # Check if any files were actually found
        if 'Contents' not in response or len(response['Contents']) == 0:
            # If no files found, return None for placeholder in frontend
            return jsonify({"url": None}), 200

        # Get the Key of the first (most relevant) match
        object_name = response['Contents'][0]['Key']

        # 4. Generate the presigned URL for the found file
        profile_pic_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )

        return jsonify({"url": profile_pic_url}), 200

    except Exception as e:
        # Standard error response if S3 connection fails
        return jsonify({"error": str(e)}), 500


@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        data = request.json or {}
        username = data.get('username')
        if not username:
            return jsonify({"error": "username is required"}), 400

        default_username = get_default_username()
        ensure_user_json_exists(default_username)
        user_json_path = get_user_json_path()

        with open(user_json_path, 'r') as f:
            user_data = json.load(f)

        users = user_data.get('users', [])
        # Prevent duplicates based on username only; return the existing user object for convenience
        existing = next((u for u in users if str(u.get('username')) == str(username)), None)
        if existing:
            return jsonify(existing), 200

        # Assign next integer user_id
        max_id = max([u.get('user_id', 0) for u in users if isinstance(u.get('user_id'), int)], default=-1)
        new_id = max(max_id + 1, 1)  # Start from 1 (0 is reserved for owner)
        
        new_user = {"user_id": new_id, "username": username}
        users.append(new_user)
        user_data['users'] = users

        tmp_path = user_json_path + '.tmp'
        with open(tmp_path, 'w') as f:
            json.dump(user_data, f, indent=4)
        os.replace(tmp_path, user_json_path)

        return jsonify(new_user), 201
    except Exception as e:
        print(f"Error in add_user: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users_aws/check', methods=['GET'])
def check_user_exists_aws():
    """Check whether a given username exists as a top-level prefix (folder) in the S3 bucket.

    Query params:
      - username: the username to check

    Returns: { "exists": true } or { "exists": false }
    """
    try:
        username = request.args.get('username')
        if not username:
            return jsonify({"error": "username is required"}), 400

        prefix = f"{username}/"

        # Use Delimiter and Prefix to efficiently check for any objects under that prefix
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, MaxKeys=1)

        exists = False
        if 'Contents' in response and len(response['Contents']) > 0:
            exists = True

        return jsonify({"exists": exists})
    except Exception as e:
        print(f"Error in check_user_exists_aws: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/friends/add', methods=['POST'])
def add_friend():
    """Add a friend to the current user's friends list by adding them to user.json.
    
    Request body:
      - friend_username: the username of the friend to add
    
    Returns: { "message": "Friend added successfully" } or error
    """
    try:
        data = request.json or {}
        friend_username = data.get('friend_username')
        
        if not friend_username:
            return jsonify({"error": "friend_username is required"}), 400
        
        current_username = get_default_username()
        if not current_username:
            return jsonify({"error": "Current user not set"}), 400
        
        # Check if friend exists in S3
        prefix = f"{friend_username}/"
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, MaxKeys=1)
        friend_exists = 'Contents' in response and len(response['Contents']) > 0
        
        if not friend_exists:
            return jsonify({"error": f"User '{friend_username}' does not exist"}), 404
        
        # Check if trying to add self
        if friend_username == current_username:
            return jsonify({"error": "Cannot add yourself as a friend"}), 400
        
        ensure_user_json_exists()
        user_json_path = get_user_json_path()
        
        with open(user_json_path, 'r') as f:
            user_data = json.load(f)
        
        users = user_data.get('users', [])
        
        # Check if friend already exists in user.json
        if any(u.get('username') == friend_username for u in users):
            return jsonify({"message": "Friend already added"}), 200
        
        # Generate next available user_id (integer > 0)
        max_user_id = max((u.get('user_id', -1) for u in users), default=-1)
        new_user_id = max(1, max_user_id + 1) if max_user_id >= 0 else 1
        
        # Add friend to user.json
        new_friend = {"user_id": new_user_id, "username": friend_username}
        users.append(new_friend)
        user_data['users'] = users
        
        tmp_path = user_json_path + '.tmp'
        with open(tmp_path, 'w') as f:
            json.dump(user_data, f, indent=4)
        os.replace(tmp_path, user_json_path)
        
        return jsonify({"message": "Friend added successfully", "friend": friend_username}), 201
    except Exception as e:
        print(f"Error in add_friend: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/friends', methods=['GET'])
def get_friends():
    """Get the current user's friends list. Returns all users with user_id > 0.
    
    Returns: { "friends": [...] } or error
    """
    try:
        ensure_user_json_exists()
        user_json_path = get_user_json_path()
        
        with open(user_json_path, 'r') as f:
            user_data = json.load(f)
        
        users = user_data.get('users', [])
        # Friends are all users with user_id > 0
        friends = [u.get('username') for u in users if u.get('user_id', 0) > 0]
        
        return jsonify({"friends": friends}), 200
    except Exception as e:
        print(f"Error in get_friends: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/current_user', methods=['GET'])
def get_current_user():
    try:
        username = get_default_username()
        if not username:
            user_json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'user.json')
            with open(user_json_path, 'r') as f:
                data = json.load(f)
            if data.get('users'):
                username = data['users'][0].get('username')
        return jsonify({'username': username})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index_page():
    try:
        screenshot_url = None
        username = get_default_username()
        if not username:
            user_json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'user.json')
            with open(user_json_path, 'r') as f:
                data = json.load(f)
            if data.get('users'):
                username = data['users'][0].get('username')
        return render_template('layout.html', username=username, screenshot_url=screenshot_url)
    except Exception as e:
        print(e)
        return "Error", 500

@app.route('/files')
def files_page():
    try:
        username = get_default_username()
        if not username:
            return "Error", 500
        files = []
        return render_template('files.html', username=username, files=files)
    except Exception as e:
        print(e)
        return "Error", 500

if __name__ == '__main__':
    # Ensure user.json is present when the app starts
    ensure_user_json_exists()
    app.run(debug=True, port=5001, host='0.0.0.0')