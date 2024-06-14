from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QPixmap, QIcon
from recording import RecorderThread

class TransparentOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.recorderThread = RecorderThread()
        self.recorderThread.recordingStopped.connect(self.onRecordingStopped)
        self.isRecording = False

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
        self.screenshotButton.setFixedSize(100, 100)  # Set fixed size for the button
        self.screenshotButton.setIcon(QIcon('icons/screenshot.svg'))
        self.screenshotButton.setIconSize(self.screenshotButton.size())
        self.screenshotButton.setStyleSheet("""
                    QPushButton {
                        background-color: lightgray;
                        border-radius: 50px;
                    }
                    QPushButton:hover {
                        background-color: gray;
                    }
                """)
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

        self.recordButton = QPushButton(buttonFrame)
        self.recordButton.setFixedSize(100, 100)
        self.recordButton.setIcon(QIcon('icons/record-start.svg'))
        self.recordButton.setIconSize(self.recordButton.size())
        self.recordButton.setStyleSheet("""
                    QPushButton {
                        background-color: lightgray;
                        border-radius: 50px;
                        font-size: 24px;
                    }
                    QPushButton:hover {
                        background-color: gray;
                    }
                """)
        self.recordButton.clicked.connect(self.toggleRecording)

        # Add the buttons to the layout
        self.layout.addWidget(self.screenshotButton)
        self.layout.addWidget(self.killSwitchButton)
        self.layout.addWidget(self.recordButton)

    def takeScreenshot(self):
        # Generate a filename with date and time
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        screenshotPath = f'output/screenshot_{now}.png'

        # Take the screenshot and save it
        screenshot = QApplication.primaryScreen().grabWindow(0)
        screenshot.save(screenshotPath, 'png')

    def toggleRecording(self):
        if self.isRecording:
            self.recorderThread.stop()
        else:
            self.recorderThread.start()
        self.isRecording = not self.isRecording

    def onRecordingStopped(self):
        self.isRecording = False

    # def toggleRecording(self):
    #     if self.recorderThread.recording:
    #         self.recordButton.setIcon(QIcon('icons/record_start.svg'))
    #     else:
    #         self.recordButton.setIcon(QIcon('icons/record_stop.svg'))
    #     self.recorderThread.toggle()

    def closeApplication(self):
        QApplication.instance().quit()