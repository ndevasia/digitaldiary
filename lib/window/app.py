from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import boto3
# from lib.globals import USERNAME
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QDateTime
from lib.recording import RecorderThread
from lib.audio import AudioRecorderThread

app = Flask(__name__)

# Folder where screenshots are saved
SCREENSHOTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../screenshots'))
# S3 Setup
s3_client = boto3.client('s3', region_name='us-west-2')
BUCKET_NAME = "digital-diary"
# Change this to your username
USERNAME = "serena"

# Global recorder instances
screen_recorder = None
audio_recorder = None

def get_screen_recorder():
    global screen_recorder
    if screen_recorder is None:
        screen_recorder = RecorderThread()
    return screen_recorder

def get_audio_recorder():
    global audio_recorder
    if audio_recorder is None:
        audio_recorder = AudioRecorderThread()
    return audio_recorder

@app.route('/generate-presigned-url', methods=['POST'])
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
    
@app.route('/')
def index():
    """Displays the latest screenshot from S3 using a pre-signed URL."""
    # List all files in the bucket with a specific prefix ("screenshot_")
    prefix = USERNAME+"/screenshot_"
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    print(response)
    
    if 'Contents' in response:
        # Filter files with prefix "screenshot_"
        files = [file for file in response['Contents'] if file['Key'].startswith(prefix)]
        
        if files:
            # Sort the files by LastModified to get the latest one
            latest_file = sorted(files, key=lambda x: x['LastModified'], reverse=True)[0]['Key']
        else:
            latest_file = None
    else:
        latest_file = None

    if latest_file:
        # Generate a pre-signed URL for the latest file
        screenshot_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': latest_file},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return render_template('layout.html', screenshot_url=screenshot_url)
    else:
        return render_template('layout.html', screenshot_url=None)

@app.route('/screenshots/<filename>')
def get_screenshot(filename):
    """Serves the screenshot file."""
    return send_from_directory(SCREENSHOTS_FOLDER, filename)

@app.route('/api/screenshot', methods=['POST'])
def take_screenshot():
    try:
        # Generate filename with date and time
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        screenshot_path = os.path.abspath(f'screenshots/screenshot_{now}.png')
        
        # Take the screenshot
        screenshot = QApplication.primaryScreen().grabWindow(0)
        screenshot.save(screenshot_path, 'png')
        
        # Upload to S3
        s3_client = boto3.client('s3', region_name='us-west-2')
        remote_path = f"{USERNAME}/screenshot_{now}.png"
        s3_client.upload_file(screenshot_path, BUCKET_NAME, remote_path)
        
        return jsonify({
            'status': 'success',
            'path': screenshot_path,
            's3_path': remote_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/start', methods=['POST'])
def start_screen_recording():
    try:
        recorder = RecorderThread()
        recorder.start()
        return jsonify({
            'status': 'started',
            'message': 'Screen recording started successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recording/stop', methods=['POST'])
def stop_screen_recording():
    try:
        recorder = RecorderThread()
        recorder.stop()
        
        # Generate thumbnail
        recorder.generate_thumbnail()
        
        # Upload video to S3
        if os.path.exists(recorder.video_path):
            s3_client = boto3.client('s3', region_name='us-west-2')
            video_name = os.path.basename(recorder.video_path)
            remote_video_path = f"{USERNAME}/{video_name}"
            s3_client.upload_file(recorder.video_path, BUCKET_NAME, remote_video_path)
            
            # Upload thumbnail if it exists
            if os.path.exists(recorder.thumbnail_path):
                thumbnail_name = os.path.basename(recorder.thumbnail_path)
                remote_thumbnail_path = f"{USERNAME}/thumbnails/{thumbnail_name}"
                s3_client.upload_file(recorder.thumbnail_path, BUCKET_NAME, remote_thumbnail_path)
        
        return jsonify({
            'status': 'stopped',
            'video_path': recorder.video_path,
            'thumbnail_path': recorder.thumbnail_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/start', methods=['POST'])
def start_audio_recording():
    try:
        audio_recorder = AudioRecorderThread()
        audio_recorder.start()
        return jsonify({
            'status': 'started',
            'message': 'Audio recording started successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/audio/stop', methods=['POST'])
def stop_audio_recording():
    try:
        audio_recorder = AudioRecorderThread()
        audio_recorder.stop()
        
        # Upload audio to S3
        if os.path.exists(audio_recorder.audio_path):
            s3_client = boto3.client('s3', region_name='us-west-2')
            audio_name = os.path.basename(audio_recorder.audio_path)
            remote_audio_path = f"{USERNAME}/audio/{audio_name}"
            s3_client.upload_file(audio_recorder.audio_path, BUCKET_NAME, remote_audio_path)
        
        return jsonify({
            'status': 'stopped',
            'audio_path': audio_recorder.audio_path
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/media', methods=['GET'])
def get_media():
    try:
        # Get query parameters for filtering
        media_type = request.args.get('media_type')
        user_id = request.args.get('user_id')
        
        MEDIA_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../model/media.json'))

        with open(MEDIA_FOLDER, 'r') as file:
            data = json.load(file)
        
        print("data", data)
        media = data['media']
        print("media", media)
        if media_type:
            media = [item for item in media if item['type'] == media_type]

        if user_id:
            media = [item for item in media if str(item['owner_user_id']) == str(user_id)]

        
        return jsonify(media)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)