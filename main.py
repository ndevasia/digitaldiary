import sys
from PyQt5.QtWidgets import QApplication
from lib.server.aws import S3
import subprocess

if __name__ == '__main__':
    client = S3()
    client.create()
    app = QApplication(sys.argv)

    sys.exit(app.exec_())
