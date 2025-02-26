import sys
from PyQt5.QtWidgets import QApplication
from lib.server.aws import S3
import subprocess

if __name__ == '__main__':
    client = S3()
    client.create()
    app = QApplication(sys.argv)

    try:
        # Run `npm run dev` to start the Electron app
        subprocess.run(['npm', 'run', 'dev'], check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error running Electron app: {e}")

    sys.exit(app.exec_())
