import pyaudio
import numpy as np
import tempfile
from pydub import AudioSegment
from time import sleep
from Controllers.Logger import Logger

class Microfono:
    def __init__(self,
                 rate=44100, chunk=1024,
                 activate=50000, deactivate=10000,
                 audioPath="microfono.wav", logger: Logger = None):
        self.rate = rate
        self.chunk = chunk
        self.activate = activate
        self.deactivate = deactivate
        self.audioPath = audioPath
        self.logger = logger

        self.pyMicro = pyaudio.PyAudio()
        self.stream = self.pyMicro.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=rate,
            input=True,
            frames_per_buffer=chunk
        )

        self.reset()

        self.levelSounds = [
            "\u001b[0m⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣀⣀⣀⣀⣠⣄⣀⣀⣀⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣀⣀⣀⣀⣤⣤⣀⣀⣀⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣀⣀⣀⣠⣤⣤⣄⣀⣀⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣀⣀⣀⣤⣤⣤⣤⣀⣀⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣄⣀⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣀⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣤⣄⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣄⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄⣀⣀\u001b[0m",
            "\u001b[32m⣀⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀⣀\u001b[0m",
            "\u001b[32m⣀⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄⣀\u001b[0m",
            "\u001b[32m⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣤⣤⣴⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣤⣴⣶⣶⣦⣤⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣤⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣴⣶⣶⣶⣶⣦⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤\u001b[0m",
            "\u001b[34m⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤\u001b[0m",
            "\u001b[34m⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤\u001b[0m",
            "\u001b[34m⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶\u001b[0m"
        ]

    def reset(self):
        self.sensibility = 1
        self.save = False
        self.audioData = []
        self.tracks = []
        self.values = []
        self.act = 0
        self.desact = 0
        self.state = 0

    def saveAudio(self):
        self.logger.log("Microphone", "Saving audio")
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio_segment = AudioSegment(
            np.array(self.tracks).tobytes(),
            frame_rate=self.rate,
            sample_width=2,
            channels=1
        )
        audio_segment.export(temp_file.name, format="wav")
        self.logger.log("Microphone", f"Audio saved to temporary file {temp_file.name}")
        return temp_file.name

    def level(self, data):
        volume = max(data) / 32767
        if volume > 1:
            volume = 1
        self.logger.log("Microphone", f"Volume level: {volume}")
        return int(volume * (len(self.levelSounds) - 1))

    def get_state(self):
        level_sound = self.level(self.values)
        state = self.levelSounds[level_sound]
        self.logger.log("Microphone", f"Current state: {state}")
        return state

    def hear(self):
        self.reset()
        while True:
            try:
                self.audioData = self.stream.read(self.chunk)
                self.values = np.frombuffer(self.audioData, dtype=np.int16)
                sound_level = max(self.values)
                if sound_level > self.activate:
                    self.act += 1
                    self.desact = 0
                elif sound_level < self.deactivate:
                    self.act = 0
                    self.desact += 1

                self.state = 1 if self.act >= self.sensibility else 0 if self.desact >= self.sensibility else self.state
                self.logger.log("Microphone", f"Sound level: {sound_level}, State: {self.state}")

                if self.state == 1:
                    self.tracks.append(self.values)
                elif self.state == 0 and self.tracks:
                    return self.saveAudio()

                sleep(0.1)
            except Exception as e:
                self.logger.log("Microphone", f"Error in hear method: {e}")
                self.reset()
                break
