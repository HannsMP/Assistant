import playsound
import pywhatkit
import os
import speech_recognition as sr
from gtts import gTTS
from Controllers.Logger import Logger
from before.Microfono import Microfono

name = "jarvis"
audioInputPath = "audioInput.wav"
audioOutputPath = "audioOutput.mp3"

log = Logger()
recog = sr.Recognizer()
micro = Microfono(output_filename=audioInputPath, threshold_start=50000, threshold_stop=2500, logger=log)


def Talk(text: str):
    try:
        tts = gTTS(f"\r{text}", lang='es-ES')
        tts.save(audioOutputPath)

        log.status = "Reproducioendo"
        log.print()

        playsound.playsound(audioOutputPath)
        os.remove(audioOutputPath)
    except Exception as e:
        log.status = "Error en la reproduccion"
        log.print()
        log.err("Error en la reproduccion\n" + e)


def Listen() -> str:
    try:

        log.status = "Escuchando"
        log.print()

        t = micro.draw()
        micro.hear()
        t.join()

        log.status = "Procesando"
        log.print()

        with sr.AudioFile(audioInputPath) as source:
            audio = recog.record(source)
            said = recog.recognize_google(audio, language='es-ES')
            return said.lower()

    except Exception as e:
        log.status = "Error en Listen"
        log.print()
        log.err(e)
        return ""


def Run():
    while True:
        try:
            say = Listen()

            if say == "":
                continue

            if not (name in say):
                continue

            enjoin = say.replace(name, '')

            if 'reproduce' in enjoin or 'reproducir' in enjoin:
                param = enjoin.replace('reproduce', '')
                log.status = "Reproduciendo..." + param
                log.print()
                Talk("Reproduciendo..." + log.status)
                pywhatkit.playonyt(param)
                continue


        except:
            pass

if __name__ == "__main__":
    Jarvis()