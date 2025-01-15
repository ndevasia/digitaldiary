from flask import Flask, render_template, send_from_directory, send_file, abort
import os
from werkzeug.utils import secure_filename
from typing import Optional

app = Flask(__name__)

# Folder where screenshots are saved
SCREENSHOTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../screenshots'))

def get_media_path(partner_id: str, media_id: str) -> Optional[str]:
    """
    Validate and return the full path to the media file
    """
    # Add validation for partner_id and media_id format
    if not all([partner_id, media_id]) or '..' in partner_id or '..' in media_id:
        return None
        
    base_path = os.path.join('path/to/media/storage', secure_filename(partner_id))
    full_path = os.path.join(base_path, secure_filename(media_id))
    
    return full_path if os.path.exists(full_path) else None

@app.route('/')
def index():
    """Displays the latest screenshot."""
    # Get the most recent screenshot from the folder
    screenshots = sorted(
        [f for f in os.listdir(SCREENSHOTS_FOLDER) if f.endswith('.png')],
        key=lambda x: os.path.getmtime(os.path.join(SCREENSHOTS_FOLDER, x)),
        reverse=True
    )
    if screenshots:
        latest_screenshot = screenshots[0]
    else:
        latest_screenshot = None

    return render_template('layout.html', screenshot=latest_screenshot)

@app.route('/screenshots/<filename>')
def get_screenshot(filename):
    """Serves the screenshot file."""
    return send_from_directory(SCREENSHOTS_FOLDER, filename)

@app.route('/api/media/download/<partner_id>/<media_id>', methods=['GET'])
def download_partner_media(partner_id, media_id):
    # Add authentication check here if needed
    # if not is_authenticated():
    #     return abort(401)
    
    media_path = get_media_path(partner_id, media_id)
    if not media_path:
        return abort(404, description="Media file not found")
    
    try:
        return send_file(
            media_path,
            as_attachment=True,
            download_name=secure_filename(f"media_{media_id}")
        )
    except Exception as e:
        app.logger.error(f"Error downloading media: {str(e)}")
        return abort(500, description="Error processing media download")

if __name__ == '__main__':
    app.run(debug=True)