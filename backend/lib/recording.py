import os
import time
import pyautogui
import cv2
import numpy as np
from PyQt5.QtCore import QDateTime, QThread, pyqtSignal
from moviepy.editor import VideoFileClip
from PIL import Image

class RecorderThread(QThread):
    started = pyqtSignal()  # Signal for when recording starts
    stopped = pyqtSignal()  # Signal for when recording stops

    def __init__(self):
        super().__init__()
        self.recording = False
        self.video_path = None
        self.thumbnail_path = None
        self.out = None

    def run(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use MP4 codec
        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        self.video_path = f"recordings/recording_{now}.mp4"
        self.thumbnail_path = f"recordings/thumbnails/recording_{now}.png"

        self.out = cv2.VideoWriter(self.video_path, fourcc, 10.0, (screen_size.width, screen_size.height))

        # Emit started signal when recording begins
        self.started.emit()

        self.recording = True
        try:
            while self.recording:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (screen_size.width, screen_size.height))

                # Check for resolution mismatch
                if frame.shape[1::-1] != (screen_size.width, screen_size.height):
                    print("Frame size mismatch!")
                    break

                self.out.write(frame)
                time.sleep(0.1)
        except Exception as e:
            print(f"Error during recording: {e}")
        finally:
            self.out.release()
            print(f"Recording finalized at {self.video_path}")

            # Emit stopped signal when recording ends
            self.stopped.emit()  # Emit stop signal when recording ends

    def stop(self):
        self.recording = False
        time.sleep(1)  # Allow pending writes to complete
        if self.out and self.out.isOpened():
            self.out.release()
            print("VideoWriter released")

    def generate_thumbnail(self):
        if not os.path.exists(self.video_path) or os.path.getsize(self.video_path) == 0:
            print(f"File {self.video_path} is invalid or incomplete.")
            return

        try:
            clip = VideoFileClip(self.video_path)
            frame_time = min(1, clip.duration / 2)
            frame = clip.get_frame(frame_time)
            image = Image.fromarray(frame)
            image.save(self.thumbnail_path)
            print(f"Thumbnail generated at {self.thumbnail_path}")
        except Exception as e:
            print(f"Failed to generate thumbnail for {self.video_path}: {e}")
