from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Skill, Experience, ContactSubmission
from django.contrib import messages
import json
import base64
import cv2
import numpy as np
from portfolio.modules import detector, controller, gaze_tracker, wink_detector
import pyjokes
import datetime
import pyautogui

# Static state to track if Jarvis is activated (shared across requests)
class JarvisState:
    is_jarvis_activated = False

def home(request):
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    return render(request, 'portfolio/index.html', {'skills': skills, 'experiences': experiences})

def about(request):
    skills = Skill.objects.all()
    experiences = Experience.objects.all()
    return render(request, 'portfolio/about.html', {'skills': skills, 'experiences': experiences})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactSubmission.objects.create(
            name=name,
            address=address,
            phone=phone,
            email=email,
            message=message
        )
        messages.success(request, 'Your message has been sent!')
        return redirect('contact')
    return render(request, 'portfolio/contact.html')

@csrf_exempt
def add_skill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        skill_name = data.get('skill')
        if skill_name:
            Skill.objects.create(name=skill_name)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Skill name is required'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt
def add_experience(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print('Received data:', data)  # Log for debugging
            position = data.get('position')
            company = data.get('company')
            years = data.get('years')
            if position and company and years is not None:
                Experience.objects.create(position=position, company=company, years=years)
                return JsonResponse({'success': True})
            return JsonResponse({'success': False, 'error': 'All fields (position, company, years) are required'})
        except json.JSONDecodeError as e:
            print('JSON error:', str(e))
            return JsonResponse({'success': False, 'error': 'Invalid JSON'})
        except ValueError as e:
            print('Value error:', str(e))
            return JsonResponse({'success': False, 'error': 'Invalid data format'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def tracker_page(request):
    """
    Renders the main tracker.html page.
    This is what the user sees when they first navigate to the URL.
    """
    return render(request, 'tracker.html')

@csrf_exempt
def process_frame(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    if 'image' not in data:
        return JsonResponse({'error': 'No image received'}, status=400)

    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    frame = cv2.flip(frame, 1)

    frame_height, frame_width = frame.shape[:2]
    print(f'Height:{frame_height}, Width: {frame_width}')

    face_landmark_detector_instance = detector.FaceLandmarkDetector()
    landmarks = face_landmark_detector_instance.detect_landmarks(frame)
    
    response = {
        'gaze': None,
        'wink': None
    }
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    cursor_instance = controller.CursorController(SCREEN_WIDTH, SCREEN_HEIGHT)
    if landmarks:
        gazeTrackerInstance = gaze_tracker.GazeTracker()
        gaze, left_iris, right_iris = gazeTrackerInstance.estimate_gaze(landmarks, frame_width, frame_height)
        if gaze and left_iris and right_iris:
            iris_x_norm = (left_iris[0] + right_iris[0]) / 2 / frame_width
            iris_y_norm = (left_iris[1] + right_iris[1]) / 2 / frame_height
            cursor_instance.move_cursor_to_iris(iris_x_norm, iris_y_norm)
            response['gaze'] = gaze
            
        wink_instance = wink_detector.WinkDetector()
        wink = wink_instance.detect_wink(landmarks, frame_width, frame_height)
        if wink:
            cursor_instance.click_if_wink(wink)
            response['wink'] = wink

    return JsonResponse(response)

def voice_assistant_page(request):
    """
    Renders the main tracker.html page.
    This is what the user sees when they first navigate to the URL.
    """
    return render(request, 'jarvis.html')

@csrf_exempt
def initialize(request):
    JarvisState.is_jarvis_activated = False
    return JsonResponse({
        "message": "Hello, I am Jarvis AI, your voice-commanded virtual assistant.",
        "speak": True,
        "open_url": None,
        "stop_recognition": False,
        "status": "Press and hold the spacebar to speak to Jarvis"
    })

@csrf_exempt
def process_command(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    try:
        data = json.loads(request.body)
        command = data.get("command", "").lower()
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    response = {
        "message": "I didn't understand that command.",
        "speak": True,
        "open_url": None,
        "stop_recognition": False,
        "status": "Press and hold the spacebar to speak to Jarvis"
    }

    if not JarvisState.is_jarvis_activated:
        if "jarvis" in command:
            JarvisState.is_jarvis_activated = True
            response["message"] = "I am ready for your command."
            response["status"] = "I am ready for your command."
        else:
            response["message"] = "Activate by calling me by my name Jarvis."
            response["status"] = "Press and hold the spacebar to speak to Jarvis"
        return JsonResponse(response)

    # Process commands when activated
    sites = [
        {"name": "youtube", "url": "https://www.youtube.com/"},
        {"name": "chat gpt", "url": "https://chatgpt.com/"},
        {"name": "github account", "url": "https://github.com/Jitenrai21"}
    ]
    for site in sites:
        if f"open {site['name']}" in command:
            response["message"] = f"Opening {site['name']}"
            response["open_url"] = site["url"]
            return JsonResponse(response)

    if "how are you" in command:
        response["message"] = "I am doing great, How are you?"
    elif "hello" in command:
        response["message"] = "Hello there. How can I help you today?"
    elif "soul mate" in command:
        response["message"] = "I believe her name is Inez."
    elif "your name" in command:
        response["message"] = "It's so silly for you to ask again. My name is Jarvis."
    elif "old are you" in command:
        response["message"] = "I have been created quite a while ago. By Jiten Rai, of course!"
    elif "time now" in command:
        time = datetime.datetime.now().strftime("%I:%M %p")
        response["message"] = f"The time is {time}"
    elif "swift" in command:
        response["message"] = "Opening Swift video"
        response["open_url"] = "https://www.youtube.com/watch?v=X_e5z_XrlzY&list=PLe9t8KT-SdWXaS4thPTG66mazDoJ2-BJq&index=3"
    elif "joke" in command:
        response["message"] = pyjokes.get_joke(language="en", category="all")
    elif "exit" in command:
        JarvisState.is_jarvis_activated = False
        response["message"] = "I am always at your service. Come again."
        response["stop_recognition"] = True
        response["status"] = "Press and hold the spacebar to speak to Jarvis"

    return JsonResponse(response)