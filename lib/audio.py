from PyQt5.QtCore import QThread, QDateTime, pyqtSignal
import sounddevice as sd
import soundfile as sf
import numpy as np

class AudioRecorderThread(QThread):
    started = pyqtSignal()  # Signal for when recording starts
    stopped = pyqtSignal()  # Signal for when recording stops

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

        # Emit started signal when audio recording begins
        self.started.emit()

        self.recording = True
        try:
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=callback):
                while self.recording:
                    sd.sleep(100)  # Sleep to allow audio recording to happen
        except Exception as e:
            print(f"Error during audio recording: {e}")
        finally:
            now = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
            self.audio_path = f"audio/audio_recording_{now}.wav"
            # Save the audio data to a file
            sf.write(self.audio_path, np.concatenate(self.frames), self.samplerate)

            # Emit stopped signal when audio recording ends
            self.stopped.emit()  # Emit stop signal when recording ends

            print(f"Audio recording finalized at {self.audio_path}")
            self.recordingStatus.emit()  # This signal might be emitted to notify that the recording is complete

    def stop(self):
        self.recording = False