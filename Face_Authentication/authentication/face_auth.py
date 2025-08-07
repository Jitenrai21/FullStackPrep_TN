import base64
import os
from io import BytesIO

import face_recognition
import numpy as np
from PIL import Image


class FaceAuthenticator:
    def __init__(self):
        self.KNOWN_FACES_DIR = "known_faces"
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """Load known faces from the known_faces directory"""
        print("Loading known faces...")

        for filename in os.listdir(self.KNOWN_FACES_DIR):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                image = face_recognition.load_image_file(
                    f"{self.KNOWN_FACES_DIR}/{filename}"
                )
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    encoding = encodings[0]
                    self.known_encodings.append(encoding)
                    self.known_names.append(os.path.splitext(filename)[0])

        print(f"Loaded {len(self.known_names)} known faces: {self.known_names}")

    def authenticate_face(self, image_data):
        """
        Authenticate a face from base64 image data
        Returns tuple: (is_authenticated, name)
        """
        try:
            # Decode base64 image
            image_data = image_data.split(",")[
                1
            ]  # Remove data:image/jpeg;base64, prefix
            image_bytes = base64.b64decode(image_data)

            # Convert to PIL Image
            pil_image = Image.open(BytesIO(image_bytes))

            # Convert to RGB numpy array
            rgb_image = np.array(pil_image.convert("RGB"))

            # Detect faces
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

            if not face_encodings:
                return False, "No face detected"

            # Compare with known faces
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_encodings, face_encoding
                )

                if True in matches:
                    face_distances = face_recognition.face_distance(
                        self.known_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]
                        return True, name

            return False, "Unknown face"

        except Exception as e:
            print(f"Error in face authentication: {e}")
            return False, f"Error: {str(e)}"
