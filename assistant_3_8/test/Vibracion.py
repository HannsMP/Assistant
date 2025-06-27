import pyaudio
import numpy as np
import matplotlib.pyplot as plt

CHUNK = 1024
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=RATE, input=True, frames_per_buffer=CHUNK)

plt.ion()  # Modo interactivo para actualizar el gráfico en tiempo real
fig, ax = plt.subplots(figsize=(8, 6))
line, = ax.plot(np.random.rand(CHUNK))

plt.title("Datos de audio en tiempo real")
plt.xlabel("Muestras")
plt.ylabel("Amplitud")

ax.set_xlim(0, CHUNK)  # Limita el eje x al tamaño del chunk
ax.set_ylim(-32768, 32767)  # Rango de valores para int16

while True:
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)

    line.set_ydata(audio_data)
    line.set_xdata(np.arange(0, CHUNK))

    ax.relim()
    ax.autoscale_view()

    plt.pause(0.01)

stream.stop_stream()
stream.close()
p.terminate()