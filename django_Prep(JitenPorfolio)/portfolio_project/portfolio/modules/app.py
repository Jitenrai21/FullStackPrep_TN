import os, sys
import cv2
import base64
import pyautogui
import numpy as np
from flask import Flask, render_template, request, jsonify

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.detector import FaceLandmarkDetector
from modules.gaze_tracker import GazeTracker
from modules.wink_detector import WinkDetector
from modules.controller import CursorController

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
screen_width, screen_height = pyautogui.size()

# Initialize detection modules
detector = FaceLandmarkDetector()
gaze_tracker = GazeTracker()
wink_detector = WinkDetector(blink_threshold=0.2, min_wink_duration=1.0)
controller = CursorController(screen_width, screen_height)  # Adjust as per your display

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image received'}), 400

    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    np_arr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    frame = cv2.flip(frame, 1)
    # print("Received frame")

    frame_height, frame_width = frame.shape[:2]
    landmarks = detector.detect_landmarks(frame)
    # print("Landmarks detected:", landmarks is not None)
    
    response = {
        'gaze': None,
        'wink': None
    }

    if landmarks:
        # Gaze estimation
        gaze, left_iris, right_iris = gaze_tracker.estimate_gaze(landmarks, frame_width, frame_height)
        # print("Gaze:", gaze)
        if gaze and left_iris and right_iris:
            iris_x_norm = (left_iris[0] + right_iris[0]) / 2 / frame_width
            iris_y_norm = (left_iris[1] + right_iris[1]) / 2 / frame_height
            controller.move_cursor_to_iris(iris_x_norm, iris_y_norm)
            response['gaze'] = gaze
            
        # Wink detection
        wink = wink_detector.detect_wink(landmarks, frame_width, frame_height)
        # print("Wink detected:", wink)
        if wink:
            controller.click_if_wink(wink)
            response['wink'] = wink

    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)

# python -m web.app