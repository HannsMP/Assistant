import pyaudio
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

plt.ion()  # Modo interactivo para actualizar el gráfico en tiempo real
fig, ax = plt.subplots(figsize=(8, 6))
(line,) = ax.plot([], [])

plt.title("Espectro de audio en tiempo real")
plt.xlabel("Frecuencia (Hz)")
plt.ylabel("Amplitud")

ax.set_xlim(0, RATE / 2)  # Limita el eje x al rango de frecuencias audibles
ax.set_ylim(0, 500000)  # Ajusta el eje

while True:
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)

    # Aplica la STFT (puedes usar otras funciones como np.fft.fft)
    spectrum = np.abs(np.fft.fft(audio_data))

    # Actualiza los datos del gráfico
    line.set_data(np.arange(len(spectrum)) * RATE / CHUNK, spectrum)

    # Pausa breve para actualizar el gráfico
    plt.pause(0.01)