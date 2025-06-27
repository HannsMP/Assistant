import pyaudio
import numpy as np
import os
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
            "\u001b[32m⣀⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣀\u001b[0m",
            "\u001b[32m⣠⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣄\u001b[0m",
            "\u001b[32m⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣤⣤⣴⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣤⣴⣶⣶⣦⣤⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣤⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣴⣶⣶⣶⣶⣦⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣦⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤⣤\u001b[0m",
            "\u001b[34m⣤⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤⣤\u001b[0m",
            "\u001b[34m⣤⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣦⣤\u001b[0m",
            "\u001b[34m⣤⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣤\u001b[0m",
            "\u001b[34m⣴⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣦\u001b[0m",
            "\u001b[34m⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣶⣶⣶⣶⣾⣷⣶⣶⣶⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶\u001b[0m",
            "\u001b[31m⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶\u001b[0m",
            "\u001b[31m⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶\u001b[0m",
            "\u001b[31m⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶\u001b[0m",
            "\u001b[31m⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷\u001b[0m",
            "\u001b[31m⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿\u001b[0m"
        ]

    def reset(self):
        self.maxKhz = 0
        self.khzMin = self.rate // 2
        self.khzMax = 0
        self.ampMax = 0
        self.state = False
        self.recording = False
        self.data = []

    def hear(self):

        self.state = True
        while self.state:
            try:
                while self.state:

                    data = self.stream.read(self.chunk)
                    audio = np.frombuffer(data, dtype=np.int16)
                    leftFft = np.fft.fft(audio)[:self.chunk // 2]
                    spectrum = np.abs(leftFft)

                    self.maxKhz = np.max(spectrum)
                    if self.recording:
                        self.data.append(data)

                        if self.maxKhz < self.deactivate:
                            self.state = False

                        continue

                    if self.maxKhz > self.activate:
                        self.recording = True
            except:
                continue

        self.reset()

    def listen(self):
        self.reset()

        self.state = True
        kHz = np.fft.fftfreq(self.chunk, 1.0 / self.rate)[:self.chunk // 2]

        while self.state:
            try:
                while self.state:

                    data = self.stream.read(self.chunk)
                    audio = np.frombuffer(data, dtype=np.int16)
                    leftFft = np.fft.fft(audio)[:self.chunk // 2]
                    spectrum = np.abs(leftFft)

                    current_max_freq = int(kHz[np.argmax(spectrum)])
                    self.khzMax = max(self.khzMax, current_max_freq)
                    self.khzMin = min(self.khzMin, current_max_freq)
                    self.ampMax = max(self.ampMax, np.max(spectrum))

                    self.maxKhz = np.max(spectrum)
                    if self.recording:
                        self.data.append(data)

                        if self.maxKhz < self.deactivate:
                            self.state = False

                        continue

                    if self.maxKhz > self.activate:
                        self.recording = True
            except:
                continue

        numChunck = len(self.data)

        return {
            "num_chunks": numChunck,
            "duration": numChunck * self.chunk / self.rate,
            "total_size": len(b''.join(self.data)),
            "max_frequency": self.khzMax,
            "min_frequency": self.khzMin,
            "max_amplitude": self.ampMax
        }

    async def printer(self, rango=100000, delay=0.1):

        lon = len(self.levelSounds) - 1

        while self.state:
            index = int(self.maxKhz // rango)
            if lon < index:
                index = lon
            self.logger.sound = self.levelSounds[index]
            sleep(delay)

        self.logger.sound = self.levelSounds[0]

    def stopstream(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pyMicro.terminate()

    def saveAudio(self) -> str:
        audio_segment = AudioSegment(
            data=b''.join(self.data),
            sample_width=2,
            frame_rate=self.rate,
            channels=1
        )

        audio_segment.export(self.audioPath, format="wav")

        return self.audioPath

    def clearAudioData(self):
        self.data = []

    def removeFile(self):
        if os.path.exists(self.audioPath):
            os.remove(self.audioPath)

    def __del__(self):
        self.stopstream()
        self.removeAudio()


# --------------------------------------------------
# ----------------------- TEST ---------------------
# --------------------------------------------------

if __name__ == "__main__":
    from Controllers.Async import Asyncrono

    Async = Asyncrono()

    log = Logger()
    mic = Microfono(logger=log, activate=200000, deactivate=0)
    line1 = Async.line(log.printer)
    line2 = Async.line(mic.printer, 5000)
    line1.start()
    line2.start()
    mic.hear()
    mic.saveAudio()
    line1.join()
    line2.join()
