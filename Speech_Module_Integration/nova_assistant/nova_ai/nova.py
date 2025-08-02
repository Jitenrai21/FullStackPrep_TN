import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import datetime
import subprocess
import sys
import pywhatkit
import random

recognizer = sr.Recognizer()

def speak(text):
    print(f"Speaking: {text}")
    tts = gTTS(text=text, lang='en')
    filename = f"temp_audio_{random.randint(1,10000)}.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

def open_software(software_name):
    if 'chrome' in software_name:
        speak('Opening Chrome...')
        subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
    elif 'microsoft edge' in software_name:
        speak('Opening Microsoft Edge...')
        subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"])
    elif 'notepad' in software_name:
        speak('Opening Notepad...')
        subprocess.Popen(['notepad.exe'])
    elif 'calculator' in software_name:
        speak('Opening Calculator...')
        subprocess.Popen(['calc.exe'])
    elif 'youtube' in software_name:
        speak('Opening YouTube...')
        pywhatkit.playonyt(software_name)
    elif 'search' in software_name:

        speak('Searching...')
        pywhatkit.search(software_name)


    elif 'instagram' in software_name:
        speak('Opening Instagram...')
        pywhatkit.playonyt(software_name)


    else:
        speak(f"I couldn't find the software {software_name}")

def close_software(software_name):
    if 'chrome' in software_name:
        speak('Closing Chrome...')
        os.system("taskkill /f /im chrome.exe")
    elif 'microsoft edge' in software_name:
        speak('Closing Microsoft Edge...')
        os.system("taskkill /f /im msedge.exe")
    elif 'notepad' in software_name:
        speak('Closing Notepad...')
        os.system("taskkill /f /im notepad.exe")
    elif 'calculator' in software_name:
        speak('Closing Calculator...')
        os.system("taskkill /f /im calculator.exe")
    else:
        speak(f"I couldn't find any open software named {software_name}")

def listen_for_wake_word():
    with sr.Microphone() as source:
        print('Listening for wake word...')
        while True:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio, language='en-US').lower()
                if 'nova' in text:
                    print('Wake word detected!')
                    speak('Hi Sir, how can I help you?')
                    return True
            except Exception as ex:
                print("Could not understand audio, please try again.")

def cmd():
    with sr.Microphone() as source:
        print('Clearing background noise... please wait!')
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print('Ask me anything...')
        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio, language='en-US').lower()
            print('Your message:', text)
        except Exception as ex:
            print("Sorry, I didn't catch that.")
            return False

    if 'stop' in text or 'exit' in text:
        speak('Terminating...I will be waiting for you!.. Goodbye!')
        sys.exit()
    elif 'open' in text:
        software_name = text.replace('open', '').strip()
        open_software(software_name)
    elif 'close' in text:
        software_name = text.replace('close', '').strip()
        close_software(software_name)
    elif 'time' in text:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        print(current_time)
        speak(current_time)
    elif 'date' in text:
        now = datetime.datetime.now()
        current_date = now.strftime("%#d %B %A")
        print(current_date)
        speak(current_date)
    elif 'who is god' in text:
        speak('Ajitheyyy Kadavuleyy, the almighty.')
    elif 'what is your name' in text:
        speak('My name is nova, your Artificial Intelligence.')
    elif 'who are you' in text:
        speak('I am Nova, your personal assistant.')
    else:
        speak("I'm Nova, I didn't understand that command.")

    return False

# Main loop
while True:
    if listen_for_wake_word():
        while True:
            cmd()
