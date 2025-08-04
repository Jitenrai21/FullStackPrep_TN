from django.shortcuts import render, redirect
from .models import Skill, Experience, ContactSubmission
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json  
import base64
import cv2
import numpy as np
from portfolio.modules import detector, controller, gaze_tracker, wink_detector
import pyautogui

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

import json
import base64
import numpy as np
import cv2
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

# You will need to replace these with your actual imports for detector,
# gaze_tracker, controller, and wink_detector.
# from .utils.gaze import GazeDetector
# from .utils.wink import WinkDetector
# from .utils.cursor_control import Controller
# from .utils.eye_tracker import GazeTracker

# Assuming these are initialized globally or passed in another way
# detector = GazeDetector()
# gaze_tracker = GazeTracker()
# wink_detector = WinkDetector()
# controller = Controller()

# The @csrf_exempt decorator is crucial for POST requests from external sources
# like a JavaScript fetch() call, as it bypasses Django's CSRF protection.
# portfolio/views.py

from django.shortcuts import render

def tracker_page(request):
    """
    Renders the main tracker.html page.
    This is what the user sees when they first navigate to the URL.
    """
    return render(request, 'tracker.html')
@csrf_exempt
# Note: This view does not have any of the video processing logic.
def process_frame(request):
    # Check if the request is a POST request
    if request.method != 'POST':
        return HttpResponseBadRequest('Invalid request method')

    try:
        # Access the raw request body and parse the JSON data
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest('Invalid JSON')

    # Check if 'image' is in the data
    if 'image' not in data:
        return JsonResponse({'error': 'No image received'}, status=400)

    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    frame = cv2.flip(frame, 1)

    frame_height, frame_width = frame.shape[:2]
    print(f'Height:{frame_height}, Width: {frame_width}')

    # You need to have your detector, gaze_tracker, etc. objects available
    # For this example, we assume they are already defined or imported.
    face_landmark_detector_instance = detector.FaceLandmarkDetector()
    landmarks = face_landmark_detector_instance.detect_landmarks(frame)
    
    response = {
        'gaze': None,
        'wink': None
    }
    SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
    cursor_instance = controller.CursorController(SCREEN_WIDTH, SCREEN_HEIGHT)
    if landmarks:
        # Gaze estimation
        gazeTrackerInstance = gaze_tracker.GazeTracker()
        gaze, left_iris, right_iris = gazeTrackerInstance.estimate_gaze(landmarks, frame_width, frame_height)
        if gaze and left_iris and right_iris:
            iris_x_norm = (left_iris[0] + right_iris[0]) / 2 / frame_width
            iris_y_norm = (left_iris[1] + right_iris[1]) / 2 / frame_height
            cursor_instance.move_cursor_to_iris(iris_x_norm, iris_y_norm)
            response['gaze'] = gaze
            
        # Wink detection
        wink_instance = wink_detector.WinkDetector()
        wink = wink_instance.detect_wink(landmarks, frame_width, frame_height)
        if wink:
            cursor_instance.click_if_wink(wink)
            response['wink'] = wink

    # Return the JSON response
    return JsonResponse(response)
