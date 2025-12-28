import pyttsx3
import speech_recognition as sr
import pyaudio
import webbrowser
import os
import datetime
import time
import psutil
import ctypes
import screen_brightness_control as sbc

from groq_api import ask_groq

from colorama import Fore, Style, init
init(autoreset=True)

"""
Listen -> Convert to Text -> Process -> Check conditions -> Respond accordingly
"""

"""Listen function to capture audio and convert to text"""
def listen():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        print(Fore.CYAN + "[●] " + Style.BRIGHT + "Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(Fore.RED + Style.BRIGHT + "[●] " + "User command: ", end="")
        print(command)
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None
    except sr.RequestError:
        print("Could not request results; check your network connection.")
        return None
        

"""Speak function to convert text to speech"""
def speak(audio_text):
    engine = pyttsx3.init()

    # Natural voice tuning
    engine.setProperty('rate', 180)    # Speach rate = 180 wpm
    engine.setProperty('volume', 0.8)  # Volume 80% 

    time.sleep(0.3)
    print(Fore.GREEN + "[●] " + Style.BRIGHT + "Jarvis: ", end="")
    print(audio_text + "\n")
    engine.say(audio_text)
    engine.runAndWait()


"""Website opener function"""
def open_website(command):
    if "youtube" in command:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
        
    elif "google" in command:
        speak("Opening Google...")
        webbrowser.open("https://www.google.com")
        
    elif "pw" in command:
        speak("Opening PW Skills...")
        webbrowser.open("https://pwskills.com/dashboard/mycourse/")
        
    elif "github" in command:
        speak("Opening your Github profile...")
        webbrowser.open("https://github.com/SrinathNeogi")
    
    elif "linkedin" in command:
        speak("Opening your LinkedIn profile...")
        webbrowser.open("https://www.linkedin.com/in/srinath-neogi-7b3a06255/")
    elif "drive" in command:
        speak("Opening Google Drive...")
        webbrowser.open("https://drive.google.com/drive/my-drive")
    elif "personal gmail" in command or "my gmail" in command or "gmail" in command:
        speak("Opening your Gmail...")
        webbrowser.open("https://mail.google.com/mail/u/0/?ogbl#inbox")
    else :
        speak("Website not recognized.")



"""Application launcher function for windows apps and installed apps""" 
def launch_app(command):
    apps = {
        "chrome" : {
            "path" : r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk",
            "speech" : "Launching Google Chrome..."
        },
        "calculator" : {
            "path" : r"calc.exe",
            "speech" : "Launching Calculator..."
        },
        "notepad" : {
            "path" : r"notepad.exe",
            "speech" : "Launching Notepad..."
        },
        "cmd" : {
            "path" : r"C:\Windows\System32\cmd.exe",
            "speech" : "Launching Command Prompt..."
        },
        "powershell" : {
            "path" : r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe",
            "speech" : "Launching PowerShell..."
        },
        "camera" : {
            "path" : "microsoft.windows.camera:",
            "speech" : "Launching Camera..."
        },
        "settings" : {
            "path" : "ms-settings:",
            "speech" : "Launching Settings..."
        },
        "task manager" : {
            "path" : r"C:\Windows\System32\Taskmgr.exe",
            "speech" : "Launching Task Manager..."
        },
        "gmail" : {
            "path" : r"C:\Users\KIIT\OneDrive\Desktop\Gmail.lnk",
            "speech" : "Launching Gmail..."
        },
        "valorant" : {
            "path" : r"C:\Users\Public\Desktop\VALORANT.lnk",
            "speech" : "Launching Valorant..."
        },
        "brave" : {
            "path" : r"C:\Users\Public\Desktop\Brave.lnk",
            "speech" : "Launching Brave Browser..."
        }
    }

    for app in apps:
        if app in command:
            speak(apps[app]["speech"])
            os.startfile(apps[app]["path"])
            return
        
    speak("Application not recognized.")

"""Greeting function"""
def greetings(command):
    if "hello" in command or "hey" in command or "hi" in command or "jarvis" in command:
        speak("Hello Sir! How can I assist you today?")
    elif "good morning" in command:
        speak("Good morning Sir! Hope you have a great day ahead.")
    elif "good evening" in command:
        speak("Good evening Sir! I hope you had a productive day.")
    elif "good night" in command:
        speak("Good night Sir! Sleep well.")
    elif "are you there" in command or "are you up" in command:
        speak("Yes Sir! Jarvis at your service.")
    elif "be ready" in command or "are you ready" in command:
        speak("Always ready Sir!")
    elif "who are you" in command or "who you are" in command:
        speak("I am Jarvis, a virtual assistant created by Srinath Neogi.")
    elif "wake up" in command:
        speak("I am awake and ready to assist you Sir!")
    elif "how are you" in command:
        speak("I am fine Sir! Ready to assist you!")
    elif "what is your name" in command or "your name" in command:
        speak("My name is Jarvis. Your personal virtual assistant.")
    elif "thank" in command:
        speak("You're welcome Sir!")
    else:
        speak("Sorry, I didn't understand that.")

    return



""""Speak date and time function to say date and time"""
def Date_time(command):

    now = datetime.datetime.now()

    day = now.strftime("%A")
    date = now.strftime("%d")
    month = now.strftime("%B")
    year = now.strftime("%y")

    time = now.strftime("%I:%M %p")

    if "date" in command:
        speak(f"Today's date is {day}, {date} {month}, {year}.")
    if "time" in command:
        speak(f"The current time is {time}.")


"""Battery status function to check battery percentage and charging status"""
def battery_status(command):
    battery = psutil.sensors_battery()

    if battery is None:
        speak("Sorry, I could not retrieve the battery information.")
        return
    
    percent = battery.percent
    plugged = battery.power_plugged

    if plugged:
        speak(f"The battery percentage is {percent} and it is charging.")
    else:
        speak(f"The battery percentage is {percent} and it is not charging.")

    if percent <= 25 and not plugged:
        speak(f"Battery is low at {percent} percent. Please plug into charger")    


""""Lock screen function to lock the system"""
def lock_system(command):
    speak("Locking the system.")
    ctypes.windll.user32.LockWorkStation()
    return



"""CPU and RAM status function to check usage"""
def cpu_ram_status(command):
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_usage = ram.percent

    if "cpu" in command:
        speak(f"The CPU usage is at {cpu_usage} percent.")
    elif "ram" in command or "memory" in command:
        speak(f"The RAM usage is at {ram_usage} percent.")



"""Wi-Fi connection status function to check if connected or disconnected"""
def wifi_connection_status():
    try:
        output = os.popen("netsh wlan show interfaces").read()

        if "State" in output and "connected" in output:
            for line in output.split("\n"):
                line = line.strip()
                if line.startswith("SSID") and "BSSID" not in line:
                    wifi_name = line.split(":", 1)[1].strip()
                    speak(f"Wi-Fi is connected to {wifi_name} network.")
                    return
        else:
            speak("Wi-Fi is disconnected.")

    except:
        speak("Unable to check Wi-Fi status.")



"""Brightness control function to set brightness level"""
def brightness_control(command):
    for word in command.split():
        if word.isdigit():
            level = int(word)
            if 0 <= level <= 100:
                speak(f"Setting brightness to {level} percent.")
                sbc.set_brightness(level)
                return
    
    speak("Please specify a brightness level between 0 and 100.")


"""search_pdf function to search pdf file in desktop """

DESKTOP_PATH = r"C:\Users\KIIT\OneDrive\Desktop"

def search_pdf(command):
    ignored_words = [
        "jarvis", "search", "for", "pdf", "file",
        "scan", "document", "on", "my", "desktop"
    ]

    words = command.lower().split()
    filtered_words = [word for word in words if word not in ignored_words]
    search_file = " ".join(filtered_words)

    found = False
    file_path = None

    for root, dirs, files in os.walk(DESKTOP_PATH):
        for file in files:
            if file.lower().endswith(".pdf") and search_file in file.lower():
                file_path = os.path.join(root, file)
                found = True
                break
        if found:
            break

    if not found:
        speak("Sorry sir, I could not find the PDF file.")
        return

    speak("Sir, I have found the PDF file.")
    speak("Do you want the file location or should I open it?")

    order = listen()
    if not order:
        speak("Sorry, I did not understand.")
        return

    order = order.lower()

    if "path" in order or "location" in order:
        speak("I have printed the file location.")
        print("PDF file location:")
        print(file_path)

    elif "open" in order or "show" in order:
        speak("Opening the PDF file.")
        os.startfile(file_path)

    else:
        speak("I am not sure what you want me to do.")


"""Internet Accessing animation"""
def internet_accessing_animation():
            
            text = "Accessing Internet"

            print(Fore.CYAN + Style.BRIGHT + "\n[ JARVIS ] ", end="")

            for char in text:
                print(Fore.GREEN + Style.BRIGHT + char, end="", flush=True)
                time.sleep(0.08)

            for _ in range(3):
                print(Fore.YELLOW + Style.BRIGHT + ".", end="", flush=True)
                time.sleep(0.5)

            print("\n")
            


"""Conditions controller function to check various conditions and call respective functions"""
def conditions_controller():
    while(True):
        audio_text = listen()
        command = audio_text.lower() if audio_text else ""

        if command is None:
            break

        if "open" in command:
            open_website(command)
            time.sleep(0.4)
        elif "launch" in command:
            launch_app(command)
            time.sleep(0.4)
        elif "search" in command or "find" in command:
            search_pdf(command)
            time.sleep(0.4)
        elif "date" in command or "time" in command:
            Date_time(command)
        elif "battery" in command:
            battery_status(command)
        elif "lock" in command:
            lock_system(command)
        elif "cpu" in command or "ram" in command or "memory" in command:
            cpu_ram_status(command)
        elif "wifi" in command or "wi-fi" in command:
            wifi_connection_status()
        elif "brightness" in command:
            brightness_control(command)
        elif "exit" in command or "quit" in command or "stop" in command or "bye" in command:
            if "exit" in command or "quit" in command or "stop" in command:
                speak("Exiting! Jarvis signing off!")
            elif "bye" in command:
                speak("Goodbye Sir! Have a great day ahead.")
            break 
        elif "information" in command or "internet" in command or "ask" in command or "groq" in command:
            speak("Yes Sir! I am ready!")

            internet_accessing_animation()

            while(True):
                ask_groq_command = listen() + "in 30 words max"

                if ask_groq_command is None:
                    speak("No command received. Exiting internet mode.")
                    break
                elif "return" in ask_groq_command or "back" in ask_groq_command or "stop" in ask_groq_command or "exit" in ask_groq_command:
                    speak("Returning to local system control.")
                    break
                else:
                    response = ask_groq(ask_groq_command)
                    speak(response)


        else:
            greetings(command)

        if "exit" in command:
            speak("Exiting! Jarvis signing off!")
            break



"""Jarvis Entry Banner function"""
def jarvis_entry_banner():
    banner = [
        "\n\n"
        "       ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗",
        "       ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝",
        "       ██║███████║██████╔╝██║   ██║██║███████╗",
        "  ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║",
        "  ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║",
        "   ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝"
    ]

    colors = [
        Fore.BLUE,
        Fore.CYAN,
        Fore.CYAN,
        Fore.CYAN,
        Fore.BLUE,
        Fore.WHITE
    ]

    for line, color in zip(banner, colors):
        print(color + Style.BRIGHT + line)
        time.sleep(0.15)

    time.sleep(0.2)
    print(
        Fore.BLUE + Style.NORMAL +
        "        Designed · Derived · Developed by " +
        Fore.CYAN + Style.BRIGHT +
        "Srinath Neogi\n"
    )

    time.sleep(0.3)
    print(Fore.GREEN + "Initializing core modules...")
    time.sleep(0.3)
    print(Fore.GREEN + "Loading speech engine...")
    time.sleep(0.3)
    print(Fore.GREEN + "Calibrating microphone...")
    time.sleep(0.3)

    print(Fore.CYAN + Style.BRIGHT + "\nStatus: ONLINE")
    print(Fore.CYAN + "Listening for commands...\n")
(Fore.CYAN + "Listening for commands...\n")


"""Jarvis Exit banner function"""
def jarvis_exit_banner():
    text = "Shutting down J.A.R.V.I.S..."


    for char in text:
        print(Fore.GREEN + Style.BRIGHT + char, end="", flush=True)
        time.sleep(0.02)

    print("\n")
    
    print(Fore.WHITE + "All systems disengaged.")
    print(Fore.CYAN + Style.BRIGHT + "Goodbye.\n")


"""Main function to run the assistant"""
def main():
    jarvis_entry_banner()
    conditions_controller()
    jarvis_exit_banner()

if __name__ == '__main__':
    main()
