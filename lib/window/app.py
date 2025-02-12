from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import boto3
from lib.globals import USERNAME

app = Flask(__name__)

# Folder where screenshots are saved
SCREENSHOTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../screenshots'))
# S3 Setup
s3_client = boto3.client('s3', region_name='us-west-2')
BUCKET_NAME = "digital-diary"
# USERNAME = "serena"


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
    print("Yes you are taking a screenshot")
    return jsonify({'test': 'test success for screenshot!'})

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