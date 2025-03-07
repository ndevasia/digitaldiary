import sys
from PyQt5.QtWidgets import QApplication
from backend.overlay import TransparentOverlay
from backend.server.aws import S3

if __name__ == '__main__':
    client = S3()
    client.create()
    app = QApplication(sys.argv)
    overlay = TransparentOverlay()
    overlay.show()
    sys.exit(app.exec_())
