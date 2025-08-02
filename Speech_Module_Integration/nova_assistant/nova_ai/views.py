from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import datetime
import os
import sys
import pywhatkit
from gtts import gTTS
import random


def home(request):
    return render(request, 'index.html')


def handle_command(text):
    response = "I'm Nova, I didn't understand that command."
    text = text.lower()

    if 'stop' in text or 'exit' in text:
        response = 'Terminating...I will be waiting for you!.. Goodbye!'

    elif 'open' in text:
        software_name = text.replace('open', '').strip()
        if 'chrome' in software_name:
            subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe"])
            response = 'Opening Chrome...'
        elif 'microsoft edge' in software_name:
            subprocess.Popen([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"])
            response = 'Opening Microsoft Edge...'
        elif 'notepad' in software_name:
            subprocess.Popen(['notepad.exe'])
            response = 'Opening Notepad...'
        elif 'calculator' in software_name:
            subprocess.Popen(['calc.exe'])
            response = 'Opening Calculator...'
        elif 'youtube' in software_name:
            pywhatkit.playonyt(software_name)
            response = 'Opening YouTube...'
        elif 'search' in software_name:
            pywhatkit.search(software_name)
            response = 'Searching...'
        elif 'instagram' in software_name:
            pywhatkit.playonyt(software_name)
            response = 'Opening Instagram...'
        else:
            response = f"I couldn't find the software {software_name}"

    elif 'close' in text:
        software_name = text.replace('close', '').strip()
        if 'chrome' in software_name:
            os.system("taskkill /f /im chrome.exe")
            response = 'Closing Chrome...'
        elif 'microsoft edge' in software_name:
            os.system("taskkill /f /im msedge.exe")
            response = 'Closing Microsoft Edge...'
        elif 'notepad' in software_name:
            os.system("taskkill /f /im notepad.exe")
            response = 'Closing Notepad...'
        elif 'calculator' in software_name:
            os.system("taskkill /f /im calculator.exe")
            response = 'Closing Calculator...'
        else:
            response = f"I couldn't find any open software named {software_name}"

    elif 'time' in text:
        response = datetime.datetime.now().strftime('%I:%M %p')
    elif 'date' in text:
        response = datetime.datetime.now().strftime("%#d %B %A")
    elif 'who is god' in text:
        response = 'Ajitheyyy Kadavuleyy, the almighty.'
    elif 'what is your name' in text:
        response = 'My name is Nova, your Artificial Intelligence.'
    elif 'who are you' in text:
        response = 'I am Nova, your personal assistant.'

    return response


@csrf_exempt
def get_response(request):
    query = request.GET.get('query', '')
    if query:
        reply = handle_command(query)
    else:
        reply = "I didn't hear any command."

    return JsonResponse({'response': reply})
