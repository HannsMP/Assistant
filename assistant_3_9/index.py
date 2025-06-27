import pyaudio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5  # Duración de la grabación

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []

print("Grabando...")

for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Grabación finalizada.")

stream.stop_stream()
stream.close()
p.terminate()

# Guardar los datos en un archivo temporal
with open("audio_temp.wav", "wb") as wf:
    wf.write(b"".join(frames))

    from gtts import gTTS

    # Cargar el archivo de audio
    audio_file = "audio_temp.wav"

    # Crear un objeto gTTS para transcribir el audio
    tts = gTTS(text="", lang="es")

    # Leer el archivo de audio y transcribirlo
    tts_text = tts.process_tts(wf.read())

    # Imprimir el texto transcribido
    print("Texto transcribido:")
    print(tts_text)
