import pyaudio
import numpy as np
import os
from pydub import AudioSegment
from time import sleep
from Controllers.Logger import Logger


class Microfono:
    def __init__(self, rate=44100, chunk=1024, threshold_start=50000, threshold_stop=10000,
                 output_filename="grabacion.wav", logger: Logger = None):
        self.rate = rate
        self.chunk = chunk
        self.start = threshold_start
        self.stop = threshold_stop
        self.filename = output_filename
        self.logger = logger
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True,
                                  frames_per_buffer=self.chunk)
        self.max = 0
        self.start = False

    def hear(self):
        recording = False
        audio_data = []

        self.start = True
        while True:
            data = self.stream.read(self.chunk)
            audio_chunk = np.frombuffer(data, dtype=np.int16)
            spectrum = np.abs(np.fft.fft(audio_chunk))[:self.chunk // 2]

            self.max = np.max(spectrum)

            if recording:
                audio_data.append(data)

                if self.max < self.stop:
                    break

            if not recording and self.max > self.start:
                recording = True
        self.start = False

        # Detener la grabación
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        # Convertir los datos de audio a un objeto AudioSegment
        audio_segment = AudioSegment(
            data=b''.join(audio_data),
            sample_width=2,
            frame_rate=self.rate,
            channels=1
        )

        # Guardar como archivo wav
        audio_segment.export(self.filename, format="wav")

    def listen(self):
        recording = False
        audio_data = []
        max_frequency = 0
        min_frequency = self.rate / 2
        max_amplitude = 0

        self.start = True

        while True:
            data = self.stream.read(self.chunk)
            audio_chunk = np.frombuffer(data, dtype=np.int16)
            spectrum = np.abs(np.fft.fft(audio_chunk))[:self.chunk // 2]

            # Calcula las frecuencias correspondientes
            freqs = np.fft.fftfreq(self.chunk, 1.0 / self.rate)[:self.chunk // 2]

            # Actualiza los valores máximos y mínimos
            current_max_freq = freqs[np.argmax(spectrum)]
            max_frequency = max(max_frequency, current_max_freq)
            min_frequency = min(min_frequency, current_max_freq)
            max_amplitude = max(max_amplitude, np.max(spectrum))

            self.max = np.max(spectrum)

            if recording:
                audio_data.append(data)

                if self.max < self.stop:
                    break

            if not recording and self.max > self.start:
                recording = True

        self.start = False

        # Detener la grabación
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        # Convertir los datos de audio a un objeto AudioSegment
        audio_segment = AudioSegment(
            data=b''.join(audio_data),
            sample_width=2,
            frame_rate=self.rate,
            channels=1
        )

        # Guardar como archivo MP3
        audio_segment.export(self.filename, format="wav")

        # Datos importantes a devolver
        duration = len(audio_data) * self.chunk / self.rate
        num_chunks = len(audio_data)
        total_size = len(b''.join(audio_data))
        recording_data = {
            "duration": duration,
            "num_chunks": num_chunks,
            "total_size": total_size,
            "max_frequency": max_frequency,
            "min_frequency": min_frequency,
            "max_amplitude": max_amplitude
        }

        return recording_data

    async def sound(self, rango=100000, delay=0.1):

        sym = [
            "--------------------",
            "---------==---------",
            "---------<>---------",
            "---------||---------",
            "--------=||=--------",
            "--------<||>--------",
            "--------||||--------",
            "-------=||||=-------",
            "-------<||||>-------",
            "-------||||||-------",
            "------=||||||=------",
            "------<||||||>------",
            "------||||||||------",
            "-----=||||||||=-----",
            "-----<||||||||>-----",
            "-----||||||||||-----",
            "----=||||||||||=----",
            "----<||||||||||>----",
            "----||||||||||||----",
            "---=||||||||||||=---",
            "---<||||||||||||>---",
            "---||||||||||||||---",
            "--=||||||||||||||=--",
            "--<||||||||||||||>--",
            "--||||||||||||||||--",
            "-=||||||||||||||||=-",
            "-<||||||||||||||||>-",
            "-||||||||||||||||||-",
            "=||||||||||||||||||=",
            "<||||||||||||||||||>",
            "||||||||||||||||||||"
        ]

        lon = len(sym)

        while self.start:
            index = self.max // rango
            if lon < index:
                index = lon
            self.logger.sound = f"\r{sym[index]} level: {index}"
            sleep(delay)


def __del__(self):
    if os.path.exists(self.filename):
        os.remove(self.filename)


if __name__ == "__main__":
    mic = Microfono(
        output_filename="../audio.wav",
        threshold_start=200000,
        threshold_stop=0
    )

    p = mic.draw(
        delay=0.1
    )
    print("Escuchando...")
    mic.hear()
    print("...Terminado")
    p.join()
