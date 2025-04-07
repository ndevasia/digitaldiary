from flask import Flask, jsonify, request, send_from_directory
import os
import boto3
import json
import sys
from flask_cors import CORS
import pyautogui
from datetime import datetime
import cv2
import numpy as np
from moviepy.editor import VideoFileClip
from PIL import Image
import requests
from PyQt5.QtCore import QDateTime  # Add this for consistent datetime formatting

app = Flask(__name__)
CORS(app)

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

# Remove sounddevice-related code since it's not used in overlay.py
# Remove: import sounddevice as sd
# Remove: import soundfile as sf

@app.route('/api/screenshot', methods=['POST'])
def take_screenshot():
    try:
        # Use QDateTime for consistency with overlay.py
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        screenshot_path = os.path.join(SCREENSHOTS_DIR, f'screenshot_{now}.png')
        
        # Take screenshot using pyautogui like in overlay.py
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
        # Use QDateTime for consistency with overlay.py
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
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
                time.sleep(0.1)  # Add sleep like in overlay.py
        
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
            time.sleep(1)  # Add sleep like in overlay.py for pending writes
            video_recorder['writer'].release()
            
            # Generate thumbnail using the same method as overlay.py
            video_path = video_recorder['path']
            thumbnail_path = os.path.join(RECORDINGS_DIR, "thumbnails", 
                                        os.path.basename(video_path).replace('.mp4', '.png'))
            
            try:
                clip = VideoFileClip(video_path)
                frame = clip.get_frame(0)
                Image.fromarray(frame).save(thumbnail_path)
                clip.close()
            except Exception as e:
                print(f"Failed to generate thumbnail: {str(e)}")
            
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

# Remove audio recording endpoints since they were using sounddevice
# We should implement them using the same approach as overlay.py's AudioRecorderThread

if __name__ == '__main__':
    app.run(debug=True, port=5000) 