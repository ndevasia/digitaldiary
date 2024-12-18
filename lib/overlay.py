import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPixmap, QIcon
from .recording import RecorderThread
from .audio import AudioRecorderThread
from .window import OutputWindow
from lib.server.aws import S3

# Ensure directories exist
os.makedirs("../screenshots", exist_ok=True)
os.makedirs("../recordings", exist_ok=True)
os.makedirs("../audio", exist_ok=True)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class TransparentOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.recorderThread = RecorderThread()
        self.recorderThread.started.connect(self.onRecordingStarted)  # Connect to onRecordingStarted
        self.recorderThread.stopped.connect(self.onRecordingStopped)  # Connect to onRecordingStopped
        self.isRecording = False
        self.audioRecorderThread = AudioRecorderThread()
        self.audioRecorderThread.stopped.connect(self.onAudioRecordingStopped)
        self.audioRecorderThread.started.connect(self.onAudioStarted)
        self.isAudioRecording = False
        self.outputWindow = OutputWindow()
        s3_client_instance = S3()
        self.client = s3_client_instance.get()

    def initUI(self):
        self.setWindowTitle('Transparent Overlay')

        # Set window flags to make the window a transparent overlay
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        # Set window size to cover the right side of the screen
        screen = QApplication.primaryScreen()
        screenGeometry = screen.geometry()
        self.setGeometry(screenGeometry.width() - 300, screenGeometry.height()/4, 300, screenGeometry.height()/2)

        # Create a central widget with a transparent background
        self.centralWidget = QWidget(self)
        self.centralWidget.setStyleSheet("background-color: rgba(240, 240, 240, 50);")
        self.setCentralWidget(self.centralWidget)

        # Create a layout and set it for the central widget
        self.layout = QVBoxLayout(self.centralWidget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignTop)

        buttonFrame = QFrame(self.centralWidget)
        buttonFrame.setFixedSize(200, 200)
        buttonFrame.setStyleSheet("background:transparent;")
        buttonLayout = QVBoxLayout(buttonFrame)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setAlignment(Qt.AlignTop)

        # Create the screenshot button
        self.screenshotButton = QPushButton(self)
        self.screenshotButton.setFixedSize(200, 200)  # Set fixed size for the button
        self.screenshotButton.setIcon(QIcon(resource_path('../icons/screenshot.svg')))
        self.screenshotButton.setIconSize(self.screenshotButton.size())
        self.screenshotButton.setStyleSheet("""
                    QPushButton {
                        background-color: lightgray;
                        border-radius: 100px;
                    }
                    QPushButton:hover {
                        background-color: gray;
                    }
                """)
        self.screenshotButton.move(50, 800)
        self.screenshotButton.clicked.connect(self.takeScreenshot)

        # Create the kill switch button
        self.killSwitchButton = QPushButton('X', self)
        self.killSwitchButton.setFixedSize(50, 50)  # Set fixed size for the button
        self.killSwitchButton.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(255, 0, 0);
                        border-radius: 25px;
                        font-size: 24px;
                    }
                    QPushButton:hover {
                        background-color: rgb(105, 21, 2);
                    }
                """)
        self.killSwitchButton.clicked.connect(self.closeApplication)

        self.recordButton = QPushButton(self)
        self.recordButton.setFixedSize(200, 200)
        self.recordButton.setIcon(QIcon(resource_path('../icons/record-start.svg')))
        self.recordButton.setIconSize(self.recordButton.size())
        self.recordButton.setStyleSheet("""
                    QPushButton {
                        background-color: lightgray;
                        border-radius: 100px;
                        font-size: 24px;
                    }
                    QPushButton:hover {
                        background-color: gray;
                    }
                """)
        self.recordButton.move(50, 400)
        self.recordButton.clicked.connect(self.toggleRecording)

        self.audioButton = QPushButton(self)
        self.audioButton.setFixedSize(200,200)
        self.audioButton.setIcon(QIcon(resource_path('../icons/audio-start.svg')))
        self.audioButton.setIconSize(self.audioButton.size())
        self.audioButton.setStyleSheet("""
                            QPushButton {
                                background-color: lightgray;
                                border-radius: 100px;
                                font-size: 24px;
                            }
                            QPushButton:hover {
                                background-color: gray;
                            }
                        """)
        self.audioButton.move(50, 0)
        self.audioButton.clicked.connect(self.toggleAudio)

    def takeScreenshot(self):
        # Generate a filename with date and time
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        screenshotPath = f'screenshots/screenshot_{now}.png'

        # Take the screenshot and save it
        screenshot = QApplication.primaryScreen().grabWindow(0)
        screenshot.save(screenshotPath, 'png')
        self.client.upload(screenshotPath)
        self.outputWindow.show()
        self.outputWindow.showScreenshot(screenshotPath)

    def toggleRecording(self):
        if self.isRecording:
            self.recorderThread.stop()

            # Generate the thumbnail after stopping the recording
            # now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
            self.recorderThread.generate_thumbnail()
        else:
            self.recorderThread.start()
        self.isRecording = not self.isRecording

    def toggleAudio(self):
        if self.isAudioRecording:
            self.audioRecorderThread.stop()
        else:
            self.audioRecorderThread.start()
        self.isAudioRecording = not self.isAudioRecording

    def onRecordingStopped(self):
        self.recordButton.setIcon(QIcon(resource_path('../icons/record-start.svg')))
        self.client.upload(self.recorderThread.video_path)
        self.client.upload(self.recorderThread.thumbnail_path)
        self.outputWindow.show()
        self.outputWindow.showVideo(self.recorderThread.thumbnail_path)

    def onAudioRecordingStopped(self):
        self.audioButton.setIcon(QIcon(resource_path('../icons/audio-start.svg')))
        self.client.upload(self.audioRecorderThread.audio_path)
        self.outputWindow.show()
        self.outputWindow.showAudio(self.audioRecorderThread.audio_path)


    def onRecordingStarted(self):
        self.recordButton.setIcon(QIcon(resource_path('../icons/record-stop.svg')))
        self.isRecording = True

    def onAudioStarted(self):
        self.isAudioRecording = True
        self.audioButton.setIcon(QIcon(resource_path('../icons/record-stop.svg')))

    def closeApplication(self):
        QApplication.instance().quit()