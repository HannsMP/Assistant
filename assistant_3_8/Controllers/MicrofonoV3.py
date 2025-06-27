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
                 logger: Logger = None):
        self.rate = rate
        self.chunk = chunk
        self.activate = activate
        self.deactivate = deactivate
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
                        self.logger.status = "Escuchando"
            except:
                continue

        self.reset()

    async def printer(self, rango=100000, delay=0.1):

        lon = len(self.levelSounds) - 1

        while self.state:
            index = int(self.maxKhz // rango)
            if lon < index:
                index = lon
            self.logger.sound = self.levelSounds[index]
            sleep(delay)

        self.logger.sound = self.levelSounds[0]

    def saveAudio(self) -> str:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio_segment = AudioSegment(
            data=b''.join(self.data),
            sample_width=2,
            frame_rate=self.rate,
            channels=1
        )

        audio_segment.export(temp_file.name, format="wav")
        return temp_file.name

# --------------------------------------------------
# ----------------------- TEST ---------------------
# --------------------------------------------------

if __name__ == "__main__":
    from Controllers.Async import Asyncrono

    Async = Asyncrono()

    log = Logger()
    mic = Microfono(logger=log, activate=200000, deactivate=0)
    line1 = Async.line(log.printer)
    line2 = Async.line(mic.printer, 10000)
    line1.start()
    line2.start()
    mic.hear()
    mic.saveAudio()
    line1.join()
    line2.join()
