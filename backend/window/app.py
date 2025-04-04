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

# Fix issue where sys.stdin, sys.stdout, or sys.stderr is None in PyInstaller
if sys.stdin is None:
    sys.stdin = open(os.devnull)
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

app = Flask(__name__)
CORS(app)  # Enable CORS to allow React app to communicate with Flask

# S3 Setup
s3_client = boto3.client('s3', region_name='us-west-2')
BUCKET_NAME = "digital-diary"
USERNAME = "sophia"

# Create necessary directories
RECORDINGS_DIR = os.path.abspath("../recordings")
SCREENSHOTS_DIR = os.path.abspath("../screenshots")
AUDIO_DIR = os.path.abspath("../audio")
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(os.path.join(RECORDINGS_DIR, "thumbnails"), exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# Global variables for recording state
video_recorder = None
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
        global video_recorder
        
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        video_path = os.path.join(RECORDINGS_DIR, f'recording_{now}.mp4')
        
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        
        video_recorder = {
            'writer': cv2.VideoWriter(
                video_path,
                fourcc,
                10.0,
                (screen_size.width, screen_size.height)
            ),
            'path': video_path,
            'recording': True
        }
        
        def record_screen():
            while video_recorder['recording']:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                video_recorder['writer'].write(frame)
        
        import threading
        recording_thread = threading.Thread(target=record_screen)
        recording_thread.start()
        
        return jsonify({
            'status': 'started',
            'path': video_path
        })
    except Exception as e:
        print(f"Recording start error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/stop', methods=['POST'])
def stop_screen_recording():
    try:
        global video_recorder
        if video_recorder and video_recorder['recording']:
            video_recorder['recording'] = False
            video_recorder['writer'].release()
            
            # Generate thumbnail
            video_path = video_recorder['path']
            thumbnail_path = video_path.replace('.mp4', '_thumb.jpg')
            
            clip = VideoFileClip(video_path)
            frame = clip.get_frame(0)
            Image.fromarray(frame).save(thumbnail_path)
            clip.close()
            
            # Generate presigned URLs and upload both files
            for file_path in [video_path, thumbnail_path]:
                object_name = f"{USERNAME}/{os.path.basename(file_path)}"
                url = s3_client.generate_presigned_url(
                    'put_object',
                    Params={'Bucket': BUCKET_NAME, 'Key': object_name},
                    ExpiresIn=3600
                )
                
                with open(file_path, 'rb') as f:
                    response = requests.put(url, data=f)
                    if response.status_code != 200:
                        raise Exception(f"Failed to upload {os.path.basename(file_path)}")
            
            video_recorder = None
            return jsonify({
                'status': 'stopped',
                'video_path': video_path,
                'thumbnail_path': thumbnail_path
            })
        return jsonify({'error': 'No active recording'}), 400
    except Exception as e:
        print(f"Recording stop error: {str(e)}")
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

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')