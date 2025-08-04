import cv2
import mediapipe as mp

class FaceLandmarkDetector:
    def __init__(self, static_mode=False, max_faces=1, detection_confidence=0.5, tracking_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh # Loads the MediaPipe FaceMesh module.
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=static_mode,
            max_num_faces=max_faces,
            refine_landmarks=True,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

    def detect_landmarks(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        landmarks = []
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                landmarks = face_landmarks.landmark
                break  # Use only the first face for now
        return landmarks
