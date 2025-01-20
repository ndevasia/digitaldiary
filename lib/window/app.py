from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import boto3

app = Flask(__name__)

# Folder where screenshots are saved
SCREENSHOTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../screenshots'))
# S3 Setup
s3_client = boto3.client('s3', region_name='us-west-2')
BUCKET_NAME = "digital-diary"


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
    """Displays the latest screenshot from S3."""
    # List all files in the bucket
    response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix="user123/")
    if 'Contents' in response:
        files = sorted(
            response['Contents'],
            key=lambda x: x['LastModified'],
            reverse=True
        )
        latest_file = files[0]['Key']
    else:
        latest_file = None

    if latest_file:
        # Download the latest file to display
        download_path = f"static/{latest_file.split('/')[-1]}"
        s3_client.download_file(BUCKET_NAME, latest_file, download_path)
        return render_template('layout.html', screenshot=download_path)
    else:
        return render_template('layout.html', screenshot=None)

@app.route('/screenshots/<filename>')
def get_screenshot(filename):
    """Serves the screenshot file."""
    return send_from_directory(SCREENSHOTS_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)