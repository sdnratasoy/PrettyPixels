"""
MediaPipe Face Mesh wrapper for face detection and landmark extraction
"""
import cv2
import mediapipe as mp
from ..utils.config import FACE_DETECTION_CONFIDENCE, MAX_NUM_FACES


class FaceDetector:
    """Wrapper for MediaPipe Face Mesh to detect faces and extract landmarks"""

    def __init__(self):
        """Initialize MediaPipe Face Mesh"""
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=MAX_NUM_FACES,
            refine_landmarks=True,
            min_detection_confidence=FACE_DETECTION_CONFIDENCE
        )

    def detect(self, image):
        """
        Detect face and extract 468 landmarks

        Args:
            image: OpenCV BGR image

        Returns:
            List of (x, y) pixel coordinates or None if no face detected
        """
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        results = self.face_mesh.process(rgb_image)

        if not results.multi_face_landmarks:
            return None

        face_landmarks = results.multi_face_landmarks[0]

        h, w = image.shape[:2]
        landmarks = []
        for landmark in face_landmarks.landmark:
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            landmarks.append((x, y))

        return landmarks

    def get_pixel_coords(self, landmarks, width, height):
        """
        Convert normalized landmarks to pixel coordinates

        Args:
            landmarks: MediaPipe normalized landmarks
            width: Image width
            height: Image height

        Returns:
            List of (x, y) pixel coordinates
        """
        pixel_coords = []
        for landmark in landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            pixel_coords.append((x, y))
        return pixel_coords
