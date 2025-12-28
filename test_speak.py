import pyttsx3

def main():
    engine = pyttsx3.init()

    engine.say("I can speak now.")
    engine.runAndWait()

if __name__ == '__main__':
    main()