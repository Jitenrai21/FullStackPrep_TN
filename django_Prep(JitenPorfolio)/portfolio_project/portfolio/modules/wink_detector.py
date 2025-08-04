import time

class WinkDetector:
    def __init__(self, blink_threshold=0.2, min_wink_duration=1.0):
        self.blink_threshold = blink_threshold # Threshold for EAR below which the eye is considered closed
        self.min_wink_duration = min_wink_duration # Minimum duration (in seconds) the eye must stay closed to count as a wink
        self.left_eye_closed_since = None
        self.right_eye_closed_since = None
        self.last_detected_wink = None

    def eye_aspect_ratio(self, eye_landmarks, frame_width, frame_height):
        y1 = int(eye_landmarks[1].y * frame_height)
        y2 = int(eye_landmarks[5].y * frame_height)
        vertical = abs(y2 - y1)

        x1 = int(eye_landmarks[0].x * frame_width)
        x2 = int(eye_landmarks[3].x * frame_width)
        horizontal = abs(x2 - x1)

        if horizontal == 0:
            return 0
        return vertical / horizontal

    def detect_wink(self, landmarks, frame_width, frame_height):
        LEFT_EYE = [33, 160, 158, 133, 153, 144]
        RIGHT_EYE = [362, 385, 387, 263, 373, 380]

        left_ear = self.eye_aspect_ratio([landmarks[i] for i in LEFT_EYE], frame_width, frame_height)
        right_ear = self.eye_aspect_ratio([landmarks[i] for i in RIGHT_EYE], frame_width, frame_height)

        now = time.time()
        wink_detected = None

        # Check left eye
        if left_ear < self.blink_threshold and right_ear >= self.blink_threshold:
            if self.left_eye_closed_since is None:
                self.left_eye_closed_since = now
            elif now - self.left_eye_closed_since >= self.min_wink_duration:
                if self.last_detected_wink != 'left':
                    wink_detected = 'left'
                    self.last_detected_wink = 'left'
        else:
            self.left_eye_closed_since = None

        # Check right eye
        if right_ear < self.blink_threshold and left_ear >= self.blink_threshold:
            if self.right_eye_closed_since is None:
                self.right_eye_closed_since = now
            elif now - self.right_eye_closed_since >= self.min_wink_duration:
                if self.last_detected_wink != 'right':
                    wink_detected = 'right'
                    self.last_detected_wink = 'right'
        else:
            self.right_eye_closed_since = None

        # Reset last detected wink when both eyes are open
        if left_ear >= self.blink_threshold and right_ear >= self.blink_threshold:
            self.last_detected_wink = None

        return wink_detected
