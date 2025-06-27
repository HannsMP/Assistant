import pyaudio
import numpy as np
from pydub import AudioSegment

CHUNK = 1024
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

recording = False
audio_data = []

print("Escuchando...")
while True:
    data = stream.read(CHUNK)
    spectrum = np.abs(np.fft.fft(np.frombuffer(data, dtype=np.int16)))

    if np.max(spectrum) > 50000:
        recording = True
        audio_data.append(data)
    elif recording and np.max(spectrum) < 10000:
        print("...Termine")
        break

# Detener la grabación
stream.stop_stream()
stream.close()
p.terminate()

# Convertir los datos de audio a un objeto AudioSegment
audio_segment = AudioSegment(
    data=b''.join(audio_data),
    sample_width=2,
    frame_rate=RATE,
    channels=1
)

# Guardar como archivo MP3
audio_segment.export("grabacion.mp3", format="mp3")
print("Grabación guardada como grabacion.mp3")