import time
import pyautogui
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QDateTime, QThread, pyqtSignal
from moviepy.editor import VideoFileClip
from PIL import Image

class RecorderThread(QThread):
    recordingStatus = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.recording = False
        self.video_path = None
        self.thumbnail_path = None

    def run(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        self.video_path = f"recordings/recording_{now}.avi"
        self.thumbnail_path = f"recordings/thumbnails/recording_{now}.png"
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

    def generate_thumbnail(self):
        try:
            # Load the video file
            clip = VideoFileClip(self.video_path)

            # Get a frame at the 1-second mark (or the 0.5-second mark if the video is too short)
            frame_time = min(1, clip.duration / 2)
            frame = clip.get_frame(frame_time)

            # Save the frame as an image
            image = Image.fromarray(frame)
            image.save(self.thumbnail_path)

            print(f"Thumbnail generated at {self.thumbnail_path}")
        except Exception as e:
            print(f"Failed to generate thumbnail for {self.video_path}: {e}")