import subprocess
import sys
import time
import requests
from lib.window.app import app
import multiprocessing
from PyQt5.QtWidgets import QApplication
from lib.overlay import TransparentOverlay
from lib.server.aws import S3

def start_flask_server():
    app.run(port=5000)

def is_server_running():
    try:
        #requests.get('http://127.0.0.1:5000')
        requests.get('http://localhost:5000/generate-presigned-url'),

        return True
    except requests.exceptions.ConnectionError:
        return False

def main():
    # Start Flask server in a separate process
    server_process = multiprocessing.Process(target=start_flask_server)
    server_process.start()

    # Wait for server to start
    print("Starting Flask server...")
    retries = 5
    while retries > 0 and not is_server_running():
        time.sleep(1)
        retries -= 1

    if not is_server_running():
        print("Failed to start Flask server")
        server_process.terminate()
        sys.exit(1)

    print("Flask server is running")

    # Your existing main application code here
    client = S3()
    client.create()
    app = QApplication(sys.argv)
    overlay = TransparentOverlay()
    overlay.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
