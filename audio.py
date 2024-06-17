from PyQt5.QtCore import QThread, QDateTime
import sounddevice as sd
import soundfile as sf
import numpy as np

class AudioRecorderThread(QThread):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.frames = []
        self.samplerate = 44100
        self.channels = 2

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
        audio_path = f"output/audio_recording_{now}.wav"
        sf.write(audio_path, np.concatenate(self.frames), self.samplerate)

    def stop(self):
        self.recording = False