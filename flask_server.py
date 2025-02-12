# flask_server.py for overlay backend
from flask import Flask, jsonify, send_file
from flask_cors import CORS
import threading
from lib.audio import AudioRecorderThread
from lib.recording import RecorderThread
from lib.server.aws import S3
import io


from PyQt5.QtCore import Qt, QDateTime
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFrame
import sys

app = Flask(__name__)
CORS(app)

# Initialize recorders and S3 client
audio_recorder = AudioRecorderThread()
screen_recorder = RecorderThread()
s3_client = S3()

# Media tracking
media_files = {
    'screenshots': [],
    'videos': [],
    'audio': []
}

# Existing endpoints remain the same...

# New endpoints for media handling
@app.route('/api/media/list', methods=['GET'])
def get_media_list():
    return jsonify(media_files)

@app.route('/api/media/file/<path:filepath>')
def get_media_file(filepath):
    try:
        file_stream = s3_client.download(filepath)
        return send_file(
            io.BytesIO(file_stream.read()),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=filepath.split('/')[-1]
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update the existing endpoints to track media files

# @app.route('/api/screenshot', methods=['POST'])
def take_screenshot():
    # Generate a filename with date and time
    now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
    screenshotPath = os.path.abspath(f'../screenshots/screenshot_{now}.png')

    # Take the screenshot and save it
    print("Taking screenshot")
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    w = QWidget()
    screenshot = screen.grabWindow( w.winId() )
    # screenshot = QApplication.primaryScreen().grabWindow(0)
    screenshot.save(screenshotPath, 'png')
    w.close()

    screenshot_url = S3.get_presigned_url(screenshotPath)
    # screenshot_url = self.client.get_presigned_url(screenshotPath)
    print(f"Screenshot URL: {screenshot_url}")  # Debugging: check if the URL is correct

    # try:
    #     with open(screenshotPath, 'rb') as f:
    #         response = requests.put(screenshot_url, data=f)
    #         if response.status_code == 200:
    #             print("Screenshot uploaded successfully.")
    #         else:
    #             print(f"Failed to upload screenshot. Status Code: {response.status_code}, Response: {response.text}")
    # except Exception as e:
    #     print(f"Error uploading screenshot: {str(e)}")


    # print("Yes you are taking a screenshot")
    # return jsonify({'test': 'test success!'})
    # try:
    #     # Your existing screenshot logic
    #     screenshot_path = f"screenshots/screenshot_{timestamp}.png"
    #     # After saving screenshot
    #     s3_client.upload(screenshot_path)
    #     media_files['screenshots'].append({
    #         'path': screenshot_path,
    #         'timestamp': timestamp
    #     })
    #     return jsonify({"path": screenshot_path})
    # except Exception as e:
    #     return jsonify({"error": str(e)}), 500

@app.route('/api/recording/stop', methods=['POST'])
def stop_screen_recording():
    if screen_recorder.isRunning():
        screen_recorder.stop()
        while screen_recorder.isRunning():
            threading.sleep(0.1)
        screen_recorder.generate_thumbnail()
        
        # Upload to S3
        s3_client.upload(screen_recorder.video_path)
        s3_client.upload(screen_recorder.thumbnail_path)
        
        # Track the video
        media_files['videos'].append({
            'path': screen_recorder.video_path,
            'thumbnail_path': screen_recorder.thumbnail_path,
            'timestamp': screen_recorder.video_path.split('_')[1].split('.')[0]
        })
        
        return jsonify({
            "status": "stopped",
            "video_path": screen_recorder.video_path,
            "thumbnail_path": screen_recorder.thumbnail_path
        })
    return jsonify({"error": "Not recording"}), 400

@app.route('/api/audio/stop', methods=['POST'])
def stop_audio_recording():
    if audio_recorder.isRunning():
        audio_recorder.stop()
        while audio_recorder.isRunning():
            threading.sleep(0.1)
            
        # Upload to S3
        s3_client.upload(audio_recorder.audio_path)
        
        # Track the audio file
        media_files['audio'].append({
            'path': audio_recorder.audio_path,
            'timestamp': audio_recorder.audio_path.split('_')[1].split('.')[0]
        })
        
        return jsonify({
            "status": "stopped",
            "path": audio_recorder.audio_path
        })
    return jsonify({"error": "Not recording"}), 400

if __name__ == '__main__':
    app.run(port=5050, debug=True)