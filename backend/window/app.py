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
        
        # Use QDateTime exactly like in RecorderThread
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        
        # Use exact same paths as RecorderThread but with full paths
        video_path = os.path.join(RECORDINGS_DIR, f"recording_{now}.mp4")
        thumbnail_path = os.path.join(THUMBNAILS_DIR, f"recording_{now}.png")
        
        # Store relative paths for S3 compatibility with overlay.py
        relative_video_path = f"recordings/recording_{now}.mp4"
        relative_thumbnail_path = f"recordings/thumbnails/recording_{now}.png"
        
        print("VIDEO WRITER BEING CALLED")  # Same log as in RecorderThread
        
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Same codec as RecorderThread
        
        # Create writer exactly like in RecorderThread
        writer = cv2.VideoWriter(
            video_path,
            fourcc,
            10.0,  # Same framerate
            (screen_size.width, screen_size.height)
        )
        
        if not writer.isOpened():
            print("Failed to create VideoWriter")
            return jsonify({'error': "Failed to create video writer"}), 500
        
        # Store the same properties as RecorderThread
        video_recorder = {
            'writer': writer,
            'path': video_path,
            'thumbnail_path': thumbnail_path,
            'relative_path': relative_video_path,
            'relative_thumbnail_path': relative_thumbnail_path,
            'recording': True,
            'screen_size': screen_size
        }
        
        # Define recording function exactly like in RecorderThread.run()
        def record_screen():
            try:
                while video_recorder and video_recorder['recording']:
                    img = pyautogui.screenshot()
                    frame = np.array(img)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Same resolution mismatch check as in RecorderThread
                    if frame.shape[1::-1] != (screen_size.width, screen_size.height):
                        print("Frame size mismatch!")
                        break
                    
                    video_recorder['writer'].write(frame)
                    time.sleep(0.1)  # Same sleep time
            except Exception as e:
                print(f"Error during recording: {e}")
            finally:
                # Same cleanup as in RecorderThread.run()
                if video_recorder and video_recorder['writer'] and video_recorder['writer'].isOpened():
                    video_recorder['writer'].release()
                    print(f"Recording finalized at {video_path}")
        
        # Start recording in a separate thread (same as overlay.py threading approach)
        recording_thread = threading.Thread(target=record_screen)
        recording_thread.daemon = True
        recording_thread.start()
        
        print("onRecordingStarted called!")  # Same log as in overlay.py
        
        return jsonify({
            'status': 'started',
            'path': relative_video_path
        })
    except Exception as e:
        print(f"Recording start error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/stop', methods=['POST'])
def stop_screen_recording():
    try:
        global video_recorder
        if video_recorder and video_recorder['recording']:
            print("recording stopped")  # Same log as in overlay.py
            print(f"video path {video_recorder['path']}")  # Same log as in overlay.py
            
            # Get all paths before we do anything else
            video_path = video_recorder['path']
            thumbnail_path = video_recorder['thumbnail_path']
            relative_video_path = video_recorder['relative_path']
            relative_thumbnail_path = video_recorder['relative_thumbnail_path']
            
            # Same stop approach as RecorderThread.stop()
            video_recorder['recording'] = False
            time.sleep(1)  # Same sleep time
            
            if video_recorder['writer'] and video_recorder['writer'].isOpened():
                video_recorder['writer'].release()
                print("VideoWriter released")  # Same log
            
            # Same thumbnail generation as RecorderThread.generate_thumbnail()
            try:
                print("GENERATE THUMBNAIL CALLED !!!")
                
                if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
                    print(f"File {video_path} is invalid or incomplete.")
                    return jsonify({'error': "Video file is invalid or incomplete"}), 500
                
                # Exactly the same thumbnail generation logic
                clip = VideoFileClip(video_path)
                frame_time = min(1, clip.duration / 2)
                frame = clip.get_frame(frame_time)
                image = Image.fromarray(frame)
                image.save(thumbnail_path)
                print(f"Thumbnail generated at {thumbnail_path}")
                clip.close()
                
            except Exception as e:
                print(f"Failed to generate thumbnail for {video_path}: {e}")
                # Try a fallback method if the primary method fails
                try:
                    cap = cv2.VideoCapture(video_path)
                    success, frame = cap.read()
                    if success:
                        cv2.imwrite(thumbnail_path, frame)
                        print(f"Thumbnail generated using fallback method at {thumbnail_path}")
                    else:
                        print("Failed to read frame from video for thumbnail")
                    cap.release()
                except Exception as e2:
                    print(f"Fallback thumbnail also failed: {str(e2)}")
            
            # Import S3 client from backend.server.aws to match overlay.py usage
            try:
                from backend.server.aws import S3
                s3_client_instance = S3()
                client = s3_client_instance.get()
                
                # Generate pre-signed URL for the video file exactly as in overlay.py
                video_url = client.get_presigned_url(relative_video_path)
                print(f"Video URL: {video_url}")  # Same log
                
                with open(video_path, 'rb') as f:
                    response = requests.put(video_url, data=f)
                    if response.status_code == 200:
                        print("Video uploaded successfully.")  # Same log
                    else:
                        print(f"Failed to upload video. Status Code: {response.status_code}, Response: {response.text}")
                
                # Generate pre-signed URL for the thumbnail file
                thumbnail_url = client.get_presigned_url(relative_thumbnail_path)
                print(f"Thumbnail URL: {thumbnail_url}")  # Same log
                
                with open(thumbnail_path, 'rb') as f:
                    response = requests.put(thumbnail_url, data=f)
                    if response.status_code == 200:
                        print("Thumbnail uploaded successfully.")  # Same log
                    else:
                        print(f"Failed to upload thumbnail. Status Code: {response.status_code}, Response: {response.text}")
            except Exception as e:
                print(f"Error with S3 upload: {str(e)}")
            
            # Clear recorder
            video_recorder = None
            
            return jsonify({
                'status': 'stopped',
                'video_path': relative_video_path,
                'thumbnail_path': relative_thumbnail_path
            })
        else:
            return jsonify({'error': 'No active recording'}), 400
    except Exception as e:
        print(f"Recording stop error: {str(e)}")
        import traceback
        traceback.print_exc()  # Additional debug info
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