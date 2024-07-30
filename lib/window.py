from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout
from PyQt5.QtCore import Qt
import cv2
from lib.server.aws import S3


class OutputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Output Window')
        self.setGeometry(100, 100, 1200, 600)

        self.mainLayout = QHBoxLayout(self)

        # Group Box for Screenshots
        self.screenshotGroupBox = QGroupBox("Screenshots")
        self.screenshotLayout = QVBoxLayout()
        self.screenshotGroupBox.setLayout(self.screenshotLayout)

        # Group Box for Videos
        self.videoGroupBox = QGroupBox("Videos")
        self.videoLayout = QVBoxLayout()
        self.videoGroupBox.setLayout(self.videoLayout)

        # Group Box for Audio
        self.audioGroupBox = QGroupBox("Audio Recordings")
        self.audioLayout = QVBoxLayout()
        self.audioGroupBox.setLayout(self.audioLayout)

        # Add the group boxes to the main layout
        self.mainLayout.addWidget(self.screenshotGroupBox)
        self.mainLayout.addWidget(self.videoGroupBox)
        self.mainLayout.addWidget(self.audioGroupBox)

        self.client = S3()

    def showScreenshot(self, screenshot_path):
        file_stream = self.client.download(screenshot_path)
        image = QImage()
        image.loadFromData(file_stream.read())
        pixmap = QPixmap.fromImage(image)
        label = QLabel()
        label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        label.setAlignment(Qt.AlignCenter)
        self.screenshotLayout.addWidget(label)

    def showVideo(self, thumbnail_path):
        file_stream = self.client.download(thumbnail_path)
        image = QImage()
        image.loadFromData(file_stream.read())
        pixmap = QPixmap.fromImage(image)
        label = QLabel(f"Video recording: {thumbnail_path}")
        label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        label.setAlignment(Qt.AlignCenter)
        self.videoLayout.addWidget(label)

    def showAudio(self, audio_path):
        label = QLabel(f"Audio recording: {audio_path}")
        label.setAlignment(Qt.AlignCenter)
        self.audioLayout.addWidget(label)