from flask import Flask, jsonify, request
import os
import boto3
import json
import sys
from flask_cors import CORS  # You'll need to install flask-cors
from lib.global_variables import *
from datetime import datetime

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
    return send_from_directory(SCREENSHOTS_FOLDER, filename)

@app.route('/api/screenshot', methods=['POST'])
def take_screenshot():
    print("Yes you are taking a screenshot")
    return jsonify({'test': 'test success for screenshot!', 'path':'some_fake_path/screenshot/xxx.png'})

@app.route('/api/recording/start', methods=['POST'])
def start_screen_recording():
    print("Yes you are STARTING a screen recording")
    return jsonify({'test': 'test success for starting screen recording!', 'status':'started'})

@app.route('/api/recording/stop', methods=['POST'])
def stop_screen_recording():
    print("Yes you are STOPPING a screen recording")
    return jsonify({'test': 'test success for stopping screen recording!', 'status':'stopped'})

@app.route('/api/audio/start', methods=['POST'])
def start_audio_recording():
    print("Yes you are STARTING an audio recording")
    return jsonify({'test': 'test success for starting audio recording!', 'status':'started'})

@app.route('/api/audio/stop', methods=['POST'])
def stop_audio_recording():
    print("Yes you are STOPPING an audio recording")
    return jsonify({'test': 'test success for stopping audio recording!', 'status':'stopped'})

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