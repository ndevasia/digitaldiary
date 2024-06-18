from PyQt5.QtCore import QThread, QDateTime, pyqtSignal
import sounddevice as sd
import soundfile as sf
import numpy as np

class AudioRecorderThread(QThread):
    recordingStatus = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.recording = False
        self.frames = []
        self.samplerate = 44100
        self.channels = 2
        self.audio_path = None

    def run(self):
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.frames.append(indata.copy())

        self.recording = True
        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=callback):
            while self.recording:
                sd.sleep(100)

        now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        self.audio_path = f"audio/audio_recording_{now}.wav"
        sf.write(self.audio_path, np.concatenate(self.frames), self.samplerate)
        self.recordingStatus.emit()

    def stop(self):
        self.recording = False