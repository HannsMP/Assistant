import speech_recognition as sr
import pyttsx3, pywhatkit

name = "jarvis"
recognizer = sr.Recognizer()

engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)


def Talk(text):
    engine.say(text)
    engine.runAndWait()


def Listen():
    try:
        with sr.Microphone() as Source:
            print("Escuchando...")
            audio = recognizer.listen(Source)
            rec = recognizer.recognize_google(audio, language='es-ES')

            rec = rec.lower()

            if name in rec:
                return rec.replace(name, "")
    except:
        return ""


def run_Jarvis():
    enjoin = Listen()

    if 'reproduce' in enjoin:
        param = enjoin.replace('reproduce', '')
        print("Reproduciendo..." + param)
        Talk("Reproduciendo..." + param)
        return pywhatkit.playonyt(param)

    if 'busca' in enjoin:
        music = enjoin.replace('busca', '')


if __name__ == "__main__":
    run_Jarvis()