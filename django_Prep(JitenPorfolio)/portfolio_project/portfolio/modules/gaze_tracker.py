import numpy as np
import cv2

# These indices help locate the iris (approximate based on FaceMesh)
LEFT_IRIS = [468, 469, 470, 471]  # Inner part of left eye
RIGHT_IRIS = [473, 474, 475, 476]

LEFT_EYE = [33, 133]   # Corners of left eye
RIGHT_EYE = [362, 263] # Corners of right eye

class GazeTracker:
    def __init__(self):
        pass

    def midpoint(self, p1, p2):
        return int((p1[0] + p2[0]) / 2), int((p1[1] + p2[1]) / 2)

    def get_eye_region(self, landmarks, eye_indices, frame_width, frame_height):
        points = []
        for idx in eye_indices:
            if idx < len(landmarks):
                x = int(landmarks[idx].x * frame_width)
                y = int(landmarks[idx].y * frame_height)
                points.append((x, y))
        return points

    def get_iris_center(self, landmarks, iris_indices, frame_width, frame_height):
        x_vals = []
        y_vals = []
        for idx in iris_indices:
            if idx < len(landmarks):
                x = int(landmarks[idx].x * frame_width)
                y = int(landmarks[idx].y * frame_height)
                x_vals.append(x)
                y_vals.append(y)
        if x_vals and y_vals:
            return int(np.mean(x_vals)), int(np.mean(y_vals))
        return None

    def estimate_gaze(self, landmarks, frame_width, frame_height):
        left_eye = self.get_eye_region(landmarks, LEFT_EYE, frame_width, frame_height)
        right_eye = self.get_eye_region(landmarks, RIGHT_EYE, frame_width, frame_height)

        left_iris = self.get_iris_center(landmarks, LEFT_IRIS, frame_width, frame_height)
        right_iris = self.get_iris_center(landmarks, RIGHT_IRIS, frame_width, frame_height)

        gaze_direction = {"left": "Unknown", "right": "Unknown"}

        if left_eye and left_iris:
            x_min = left_eye[0][0]
            x_max = left_eye[1][0]
            gaze_ratio = (left_iris[0] - x_min) / (x_max - x_min + 1e-6)

            if gaze_ratio < 0.4:
                gaze_direction["left"] = "Left"
            elif gaze_ratio > 0.6:
                gaze_direction["left"] = "Right"
            else:
                gaze_direction["left"] = "Center"

        if right_eye and right_iris:
            x_min = right_eye[1][0]
            x_max = right_eye[0][0]
            gaze_ratio = (right_iris[0] - x_min) / (x_max - x_min + 1e-6)

            if gaze_ratio < 0.4:
                gaze_direction["right"] = "Right"
            elif gaze_ratio > 0.6:
                gaze_direction["right"] = "Left"
            else:
                gaze_direction["right"] = "Center"

        return gaze_direction, left_iris, right_iris