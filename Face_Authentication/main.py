import os

import cv2
import face_recognition
import numpy as np

# Load known faces
KNOWN_FACES_DIR = "known_faces"
known_encodings = []
known_names = []

print("Loading known faces...")

for filename in os.listdir(KNOWN_FACES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{filename}")
        encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(encoding)
        known_names.append(os.path.splitext(filename)[0])

# Start video capture
video = cv2.VideoCapture(0)

print("Authenticating... Press 'q' to quit.")

while True:
    ret, frame = video.read()
    if not ret:
        continue

    # Resize frame for speed
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_names[best_match_index]

        top, right, bottom, left = [
            v * 4 for v in face_location
        ]  # rescale to original size
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Authenticated: {name}",
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 255),
            2,
        )

    cv2.imshow("Face Authentication", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

print(known_encodings)
print("known names:", known_names)

video.release()
cv2.destroyAllWindows()
