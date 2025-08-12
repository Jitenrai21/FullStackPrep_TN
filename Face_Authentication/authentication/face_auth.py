import base64
import os
from io import BytesIO

import face_recognition
import numpy as np
from PIL import Image

from .models import FaceEmbedding


class FaceAuthenticator:
    def __init__(self):
        self.KNOWN_FACES_DIR = "known_faces"
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces_from_db()

    def load_known_faces_from_db(self):
        """Load known faces from the database instead of directory"""
        print("Loading known faces from database...")

        # Clear existing data
        self.known_encodings = []
        self.known_names = []

        try:
            # Get all face embeddings from database
            face_embeddings = FaceEmbedding.objects.all()

            for face_embedding in face_embeddings:
                try:
                    # Get the embedding data
                    encoding = face_embedding.get_embedding()
                    self.known_encodings.append(encoding)
                    self.known_names.append(face_embedding.name)
                except Exception as e:
                    print(f"Error loading embedding for {face_embedding.name}: {e}")
                    continue

            print(
                f"Loaded {len(self.known_names)} known faces from database: {self.known_names}"
            )

        except Exception as e:
            print(f"Error accessing database: {e}")
            # Fallback to loading from files if database fails
            self.load_known_faces_from_files()

    def load_known_faces_from_files(self):
        """Fallback method: Load known faces from the known_faces directory"""
        print("Loading known faces from files (fallback)...")

        if not os.path.exists(self.KNOWN_FACES_DIR):
            print(f"Directory {self.KNOWN_FACES_DIR} does not exist")
            return

        for filename in os.listdir(self.KNOWN_FACES_DIR):
            if filename.lower().endswith((".jpg", ".jpeg")):
                try:
                    image_path = os.path.join(self.KNOWN_FACES_DIR, filename)
                    image = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(image)
                    if encodings:
                        encoding = encodings[0]
                        self.known_encodings.append(encoding)
                        self.known_names.append(os.path.splitext(filename)[0])
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    continue

        print(
            f"Loaded {len(self.known_names)} known faces from files: {self.known_names}"
        )

    def reload_faces(self):
        """Reload faces from database - useful after admin changes"""
        self.load_known_faces_from_db()

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

            # Reload faces from database to get latest data
            self.reload_faces()

            if not self.known_encodings:
                return False, "No known faces in database"

            # Compare with known faces
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(
                    self.known_encodings, face_encoding, tolerance=0.6
                )

                if True in matches:
                    face_distances = face_recognition.face_distance(
                        self.known_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
                        print(f"Face matched: {name} with confidence: {confidence:.2f}")
                        return True, name

            return False, "Unknown face"

        except Exception as e:
            print(f"Error in face authentication: {e}")
            return False, f"Error: {str(e)}"
