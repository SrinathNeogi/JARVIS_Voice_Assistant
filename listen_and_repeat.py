import pyttsx3
import speech_recognition as sr

r = sr.Recognizer()

def main():
    engine = pyttsx3.init()

    with sr.Microphone() as source:
        print("Say something ...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said : {text}")

        engine.say(f"You said : {text}")
        engine.runAndWait()

    except:
        print("Could not understand audio")

if __name__ == '__main__':
    main()