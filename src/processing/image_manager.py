"""
Image state management for non-destructive editing
"""
import cv2
import numpy as np


class ImageManager:
    """Manages image state and processing history"""

    def __init__(self):
        """Initialize image manager"""
        self.original_image = None  # Immutable original
        self.working_image = None  # Current processed state
        self.blemish_points = []  # List of (x, y) blemish coordinates
        self.face_landmarks = None  # MediaPipe landmarks
        self.face_masks = {}  # Precomputed masks

    def load_image(self, path):
        """
        Load image from file

        Args:
            path: Path to image file
        """
        with open(path, 'rb') as f:
            file_bytes = np.frombuffer(f.read(), dtype=np.uint8)
            self.original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if self.original_image is not None:
            self.working_image = self.original_image.copy()
        self.blemish_points = []

    def set_face_data(self, landmarks, masks):
        """
        Store face detection results

        Args:
            landmarks: List of (x, y) landmark coordinates
            masks: Dictionary of facial region masks
        """
        self.face_landmarks = landmarks
        self.face_masks = masks

    def add_blemish_point(self, x, y):
        """
        Add blemish removal point

        Args:
            x: X coordinate
            y: Y coordinate
        """
        self.blemish_points.append((x, y))

    def get_original(self):
        """
        Get copy of original image

        Returns:
            Copy of original image or None if not loaded
        """
        if self.original_image is not None:
            return self.original_image.copy()
        return None

    def update_working(self, image):
        """
        Update working image with processed result

        Args:
            image: Processed image
        """
        self.working_image = image.copy()

    def reset(self):
        """Reset all effects and return to original"""
        if self.original_image is not None:
            self.working_image = self.original_image.copy()
            self.blemish_points = []
