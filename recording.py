import time
import pyautogui
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QDateTime, QThread, pyqtSignal

class RecorderThread(QThread):
    recordingStatus = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.recording = False
        self.video_path = None

    def run(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        self.video_path = f"recordings/recording_{now}.avi"
        out = cv2.VideoWriter(self.video_path, fourcc, 10.0, (screen_size.width, screen_size.height))

        self.recording = True
        while self.recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
            time.sleep(0.1)

        out.release()
        self.recordingStatus.emit()

    def stop(self):
        self.recording = False