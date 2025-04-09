from flask import Flask, jsonify, request, send_from_directory
import os
import boto3
import json
import sys
from flask_cors import CORS  # You'll need to install flask-cors
import pyautogui
from datetime import datetime
import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from PIL import Image
import requests
import sounddevice as sd  # Used in AudioRecorderThread
import soundfile as sf    # Used in AudioRecorderThread
from PyQt5.QtCore import QDateTime  # For consistent date formatting
import time
import threading
# Fix path to import from sibling directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Path being added to sys.path:", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Current sys.path:", sys.path)
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
s3_client = boto3.client('s3', region_name='us-west-2')
BUCKET_NAME = "digital-diary"
USERNAME = "sophia"

# Get the base directory (similar to how overlay.py gets to "recordings")
# This ensures we save to the project's root recordings directory
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RECORDINGS_DIR = os.path.join(base_dir, "recordings")
SCREENSHOTS_DIR = os.path.join(base_dir, "screenshots")
AUDIO_DIR = os.path.join(base_dir, "audio")
THUMBNAILS_DIR = os.path.join(RECORDINGS_DIR, "thumbnails")

# Create directories (same as in overlay.py)
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(THUMBNAILS_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Global variables for recording state
recorder_thread = None
audio_recorder = None

@app.route('/api/test', methods=['GET'])
def test_endpoint():
    return jsonify({"message": "API is working!"})

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

@app.route('/api/screenshots/<filename>')
def get_screenshot(filename):
    """Serves the screenshot file."""
    return send_from_directory(SCREENSHOTS_DIR, filename)

@app.route('/api/screenshot', methods=['POST'])
def take_screenshot():
    try:
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f'screenshot_{now}.png')
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        # Generate presigned URL for upload
        object_name = f"{USERNAME}/screenshot_{now}.png"
        url = s3_client.generate_presigned_url(
            'put_object',
            Params={'Bucket': BUCKET_NAME, 'Key': object_name},
            ExpiresIn=3600
        )
        
        # Upload to S3
        with open(screenshot_path, 'rb') as f:
            response = requests.put(url, data=f)
            if response.status_code != 200:
                raise Exception("Failed to upload screenshot")
        
        return jsonify({
            'status': 'success',
            'path': screenshot_path,
            'url': url
        })
    except Exception as e:
        print(f"Screenshot error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/start', methods=['POST'])
def start_screen_recording():
    try:
        global recorder_thread
        
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
            
            # Generate pre-signed URL for the video file
            video_url = client.get_presigned_url(recorder_thread.video_path)
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
            
            # Generate pre-signed URL for the thumbnail file
            thumbnail_url = client.get_presigned_url(recorder_thread.thumbnail_path)
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

            # Extract username from S3 path as owner_user_id
            owner_user_id = item['Key'].split('/')[0]  # Gets username from "username/filename"

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

            # Transform into your media data type format
            media_item = {
                "media_id": idx,
                "type": media_type,
                "media_url": media_url,
                "timestamp": item['LastModified'].isoformat(),
                "owner_user_id": owner_user_id,  # Using username from S3 path
                "game": "game1"
            }

            media_list.append(media_item)

        # Apply filters if provided
        media_type = request.args.get('media_type')
        if media_type:
            media_list = [item for item in media_list if item['type'] == media_type]

        return jsonify(media_list)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')