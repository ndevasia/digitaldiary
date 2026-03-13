from flask import Flask, jsonify, request, send_from_directory, render_template
import os
import boto3
import json
import sys
import signal  # Add this import for graceful shutdown
from flask_cors import CORS  # You'll need to install flask-cors
import pyautogui
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
    # Import RecorderThread
    from lib.recording import RecorderThread
    print("Successfully imported RecorderThread from recording")

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

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React app to communicate with Flask


# Helper functions for user.json
def get_user_json_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'user.json')


def get_user_id_from_username(username):
    """Convert username to integer user_id by looking it up in user.json."""
    try:
        path = get_user_json_path()
        if os.path.exists(path):
            with open(path, 'r') as f:
                data = json.load(f)
            users = data.get('users', [])
            user = next((u for u in users if u.get('username') == username), None)
            if user:
                return user.get('user_id')
    except Exception as e:
        print(f"Error getting user_id from username: {e}")
    # Return None if not found
    return None


def ensure_user_json_exists(username=None):
    """Create user.json from configured USERNAME if it doesn't exist, and ensure default is present."""
    if not username:
        username = get_default_username()
    
    try:
        if not username:
            # No configured username; nothing to ensure
            return

        path = get_user_json_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(path):
            # Create default owner with user_id 0
            default_user = {"user_id": 0, "username": username}
            tmp_path = path + '.tmp'
            with open(tmp_path, 'w') as f:
                json.dump({"users": [default_user]}, f, indent=4)
            os.replace(tmp_path, path)
            return

        # If file exists, ensure USERNAME user exists with user_id 0
        with open(path, 'r') as f:
            data = json.load(f)

        users = data.get('users', [])
        # Check if USERNAME exists with any user_id
        username_exists = any(str(u.get('username')) == str(username) for u in users)
        
        if not username_exists:
            # Find highest user_id and add new user with next ID
            max_id = max([u.get('user_id', 0) for u in users if isinstance(u.get('user_id'), int)], default=-1)
            new_id = max(max_id + 1, 1)  # Next ID, but not 0 (reserved for owner)
            users.append({"user_id": new_id, "username": username})
            data['users'] = users
            tmp_path = path + '.tmp'
            with open(tmp_path, 'w') as f:
                json.dump(data, f, indent=4)
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

# Create directories (same as in overlay.py)
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(THUMBNAILS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(PROFILE_PICS_DIR, exist_ok=True)

# Global variables for recording state
recorder_thread = None
audio_recorder = None

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

        # Load metadata overrides for this user
        try:
            metadata_response = s3_client.get_object(
                Bucket=BUCKET_NAME,
                Key=f"{prefix_username}/metadata.json"
            )
            metadata_overrides = json.loads(metadata_response["Body"].read().decode("utf-8"))
        except s3_client.exceptions.NoSuchKey:
            metadata_overrides = {}

        media_list = []
        for idx, item in enumerate(response['Contents'], 1):
            # Skip metadata.json files
            if item['Key'].endswith('metadata.json'):
                continue

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
                "session_id": session_id,
                "app_name": session_id if session_id else "app1",  # Use session_id if available, else fallback
                "s3_key": item['Key']  # Add the actual S3 key for deletion
            }

            # Apply metadata overrides if they exist
            if item['Key'] in metadata_overrides:
                media_item.update(metadata_overrides[item['Key']])

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
        prefix = username + "/"
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
def take_screenshot():
    try:
        username = get_default_username()
        data = request.json or {}
        app_name = data.get('app_name')
        user_with = data.get('user_with')
        
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f'screenshot_{now}.png')

        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)

        # Generate presigned URL for upload with session metadata in S3 path
        # Store as: username/session_id/screenshot_{timestamp}.png
        # where session_id incorporates the app info
        session_id = app_name if app_name else 'default'
        object_name = f"{username}/{session_id}/screenshot_{now}.png"
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )

        # Upload to S3 with metadata
        with open(screenshot_path, 'rb') as f:
            response = requests.put(url, data=f)
            if response.status_code != 200:
                raise Exception("Failed to upload screenshot")

        return jsonify({
            'status': 'success',
            'path': screenshot_path,
            'url': url,
            'app_name': app_name,
            'user_with': user_with
        })
    except Exception as e:
        print(f"Screenshot error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/start', methods=['POST'])
def start_screen_recording():
    try:
        global recorder_thread

        # Extract session metadata from request
        data = request.json or {}
        app_name = data.get('app_name')
        
        # Check if recording is already in progress
        if recorder_thread and recorder_thread.recording:
            return jsonify({'error': 'Recording already in progress'}), 400

        # Create a new RecorderThread instance
        recorder_thread = RecorderThread()

        # Set up signal handler for when recording stops
        def on_recording_stopped():
            print("Recording stopped signal received")
            # Create S3 client
            s3_client_instance = S3()
            client = s3_client_instance.get()

            # Generate pre-signed URL for the video file with session_id
            video_url = client.get_presigned_url(recorder_thread.video_path, session_id=app_name)
            print(f"Video URL: {video_url}")

            try:
                with open(recorder_thread.video_path, 'rb') as f:
                    response = requests.put(video_url, data=f)
                    if response.status_code == 200:
                        print("Video uploaded successfully.")
                    else:
                        print(f"Failed to upload video. Status Code: {response.status_code}, Response: {response.text}")
            except Exception as e:
                print(f"Error uploading video: {str(e)}")

            # Generate pre-signed URL for the thumbnail file with session_id
            thumbnail_url = client.get_presigned_url(recorder_thread.thumbnail_path, session_id=app_name)
            print(f"Thumbnail URL: {thumbnail_url}")

            try:
                with open(recorder_thread.thumbnail_path, 'rb') as f:
                    response = requests.put(thumbnail_url, data=f)
                    if response.status_code == 200:
                        print("Thumbnail uploaded successfully.")
                    else:
                        print(f"Failed to upload thumbnail. Status Code: {response.status_code}, Response: {response.text}")
            except Exception as e:
                print(f"Error uploading thumbnail: {str(e)}")

        # Connect signal
        recorder_thread.stopped.connect(on_recording_stopped)

        # Start recording
        recorder_thread.start()

        # Return the relative paths
        return jsonify({
            'status': 'started',
            'path': recorder_thread.video_path,
            'thumbnail_path': recorder_thread.thumbnail_path
        })
    except Exception as e:
        print(f"Recording start error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/stop', methods=['POST'])
def stop_screen_recording():
    try:
        global recorder_thread

        # Check if recording is in progress
        if not recorder_thread or not recorder_thread.recording:
            return jsonify({'error': 'No active recording'}), 400

        # Get paths before stopping
        video_path = recorder_thread.video_path
        thumbnail_path = recorder_thread.thumbnail_path

        # Stop the recording
        recorder_thread.stop()

        # Generate thumbnail
        recorder_thread.generate_thumbnail()

        # Return paths
        return jsonify({
            'status': 'stopped',
            'video_path': video_path,
            'thumbnail_path': thumbnail_path
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

        # Extract session metadata from request
        data = request.json or {}
        app_name = data.get('app_name')

        # Initialize audio recorder with the same parameters as AudioRecorderThread
        audio_recorder = {
            'recording': True,
            'frames': [],
            'samplerate': 44100,
            'app_name': app_name  # Store app_name for later use in stop
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
        username = get_default_username()
        if audio_recorder and audio_recorder['recording']:
            # Get app_name before stopping
            app_name = audio_recorder.get('app_name')
            
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
                # Use app_name as session_id in S3 path
                session_id = app_name if app_name else 'default'
                object_name = f"{username}/{session_id}/{os.path.basename(audio_path)}"
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
        user_with = data.get('userWith') or '0'  # Default to user_id 0 if empty
        
        if not app_name:
            return jsonify({"error": "appName is required"}), 400
        
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
        s3 = S3()
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

@app.route('/api/media/delete', methods=['DELETE', 'POST'])
def delete_media():
    try:
        data = request.json
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
        
        # Import aws.py's S3 class and update metadata
        from server.aws import S3
        s3 = S3()
        success = s3.update_media_metadata(s3_key, metadata)
        
        if not success:
            return jsonify({"error": "Failed to update media metadata"}), 500
        
        return jsonify({"status": "success"})
        
    except Exception as e:
        print(f"Error updating media metadata: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        # Ensure user.json exists and has the default configured USERNAME
        username = get_default_username()
        ensure_user_json_exists(username)

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
            user_json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'model', 'user.json')
            with open(user_json_path, 'r') as f:
                data = json.load(f)
            if data.get('users'):
                username = data['users'][0].get('username')
        files = []
        return render_template('files.html', username=username, files=files)
    except Exception as e:
        print(e)
        return "Error", 500

if __name__ == '__main__':
    # Ensure user.json is present for the configured USERNAME when the app starts
    ensure_user_json_exists(get_default_username())
    app.run(debug=True, port=5001, host='0.0.0.0')