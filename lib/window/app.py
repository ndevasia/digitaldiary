from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

# Folder where screenshots are saved
SCREENSHOTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../screenshots'))

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

@app.route('/files')
def files():

    return render_template('files.html')

@app.route('/screenshots/<filename>')
def get_screenshot(filename):
    """Serves the screenshot file."""
    return send_from_directory(SCREENSHOTS_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)