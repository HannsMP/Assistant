import playsound
import pywhatkit
import os
import speech_recognition as sr
from gtts import gTTS
from Controllers.Logger import Logger
from Controllers.MicrofonoV3 import Microfono
from Controllers.Async import Asyncrono


class Jarvis:
    def __init__(self):
        self.name = "jarvis"
        self.pathAudioInput = "audioInput.wav"
        self.pathAudioOutput = "audioOutput.mp3"

        self.promise = Asyncrono()
        self.logger = Logger()
        self.recognizer = sr.Recognizer()
        self.microfono = Microfono(
            audioPath=self.pathAudioInput,
            activate=100000,
            deactivate=50000,
            logger=self.logger
        )

        line = self.promise.line(self.logger.printer)
        line.start()
        self.Run()
        line.join()

        self.logger.status = "Iniciando"

        line = self.promise.line(
            self.microfono.printer,
            10000
        )

        line.start()
        line.join()

    def TTS(self, text):
        try:
            tts = gTTS(f"\r{text}", lang='es-ES')
            tts.save(self.pathAudioOutput)

            self.logger.status = "Reproducioendo"

            playsound.playsound(self.pathAudioOutput)
            os.remove(self.pathAudioOutput)
        except Exception as e:
            self.logger.status = "Error en la reproduccion"

            self.logger.err("Error en la reproduccion\n")
            self.logger.err(e)

    def STT(self) -> str:

        try:
            self.logger.status = "Esperando"
            self.microfono.hear()
            audiofile = self.microfono.saveAudio()

            self.logger.status = "Procesando"
            with sr.AudioFile(audiofile) as source:
                audio = self.recognizer.record(source)
                print(audio)
                said = self.recognizer.recognize_google(audio, language='es-ES')

                print(said)
                return said.lower()

        except Exception as e:
            self.logger.status = "Error en STT"
            self.logger.err(e)
            print(e)
            return ""

    def Run(self):
        while True:
            try:
                say = self.STT()

                if say == "":
                    continue

                if not (self.name in say):
                    continue

                enjoin = say.replace(self.name, '')

                if 'reproduce' in enjoin or 'reproducir' in enjoin:
                    param = enjoin.replace('reproduce', '')
                    status = self.logger.status = "Reproduciendo..." + param
                    self.TTS("Reproduciendo..." + status)
                    pywhatkit.playonyt(param)
                    continue


            except:
                pass


if __name__ == "__main__":
    Jarvis()
