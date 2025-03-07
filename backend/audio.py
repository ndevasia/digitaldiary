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
        # Detect the default input device
        default_device = sd.query_devices(kind='input')

        # Ensure the device supports at least 1 channel
        self.channels = min(default_device['max_input_channels'], 2)
        if self.channels < 1:
            raise ValueError("No valid input channels found on the default recording device.")

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
            print(f"Audio recording finalized at {self.audio_path}")
            self.stopped.emit()  # Emit stop signal when recording ends

    def stop(self):
        self.recording = False