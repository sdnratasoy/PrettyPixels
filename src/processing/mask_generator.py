"""
Generate masks for different facial regions using MediaPipe landmarks
"""
import cv2
import numpy as np
from ..utils.constants import (
    FACE_OVAL_INDICES,
    LIPS_INDICES,
    LEFT_EYE_INDICES,
    RIGHT_EYE_INDICES,
    LEFT_CHEEK_CENTER,
    RIGHT_CHEEK_CENTER,
    CHEEK_RADIUS_RATIO
)
from ..utils.image_utils import feather_mask


class MaskGenerator:
    """Generate masks for different facial regions"""

    def __init__(self):
        """Initialize with facial landmark indices"""
        self.face_oval = FACE_OVAL_INDICES
        self.lips = LIPS_INDICES
        self.left_eye = LEFT_EYE_INDICES
        self.right_eye = RIGHT_EYE_INDICES
        self.left_cheek_center = LEFT_CHEEK_CENTER
        self.right_cheek_center = RIGHT_CHEEK_CENTER
        self.cheek_radius_ratio = CHEEK_RADIUS_RATIO

    def generate_all_masks(self, landmarks, image_shape):
        """
        Generate all facial region masks

        Args:
            landmarks: List of (x, y) landmark coordinates
            image_shape: Shape of image (height, width, channels)

        Returns:
            Dictionary of masks: {'face', 'lips', 'cheeks', 'eyes'}
        """
        masks = {}
        masks['face'] = self.create_face_mask(landmarks, image_shape)
        masks['lips'] = self.create_lip_mask(landmarks, image_shape)
        masks['cheeks'] = self.create_cheek_masks(landmarks, image_shape)
        masks['eyes'] = self.create_eye_masks(landmarks, image_shape)
        return masks

    def create_face_mask(self, landmarks, shape):
        """
        Create face contour mask

        Args:
            landmarks: List of (x, y) coordinates
            shape: Image shape

        Returns:
            Binary mask of face region
        """
        mask = np.zeros(shape[:2], dtype=np.uint8)

        face_points = np.array([landmarks[i] for i in self.face_oval], dtype=np.int32)

        cv2.fillPoly(mask, [face_points], 255)

        mask = feather_mask(mask, kernel_size=15)

        return mask

    def create_lip_mask(self, landmarks, shape):
        """
        Create lip mask (excluding only the innermost teeth area)

        Args:
            landmarks: List of (x, y) coordinates
            shape: Image shape

        Returns:
            Binary mask of lip region (without teeth)
        """
        from ..utils.constants import (
            LIPS_UPPER_OUTER, LIPS_LOWER_OUTER,
            LIPS_UPPER_INNER, LIPS_LOWER_INNER
        )

        mask = np.zeros(shape[:2], dtype=np.uint8)

        upper_outer = np.array([landmarks[i] for i in LIPS_UPPER_OUTER], dtype=np.int32)
        lower_outer = np.array([landmarks[i] for i in LIPS_LOWER_OUTER], dtype=np.int32)

        upper_inner = np.array([landmarks[i] for i in LIPS_UPPER_INNER], dtype=np.int32)
        lower_inner = np.array([landmarks[i] for i in LIPS_LOWER_INNER], dtype=np.int32)

        outer_contour = np.vstack([upper_outer, lower_outer[::-1]])
        cv2.fillPoly(mask, [outer_contour], 255)

 
        inner_contour = np.vstack([upper_inner, lower_inner[::-1]])
        inner_mask = np.zeros(shape[:2], dtype=np.uint8)
        cv2.fillPoly(inner_mask, [inner_contour], 255)

        kernel = np.ones((3, 3), np.uint8)
        inner_mask = cv2.erode(inner_mask, kernel, iterations=3) 

        mask[inner_mask > 0] = 0

        mask = cv2.erode(mask, kernel, iterations=1)

        mask = feather_mask(mask, kernel_size=5)

        return mask

    def create_cheek_masks(self, landmarks, shape):
        """
        Create cheek masks (left and right combined)

        Args:
            landmarks: List of (x, y) coordinates
            shape: Image shape

        Returns:
            Binary mask of cheek regions
        """
        mask = np.zeros(shape[:2], dtype=np.uint8)

        face_points = np.array([landmarks[i] for i in self.face_oval])
        face_width = np.max(face_points[:, 0]) - np.min(face_points[:, 0])
        face_height = np.max(face_points[:, 1]) - np.min(face_points[:, 1])

        cheek_radius_h = int(face_width * 0.18)
        cheek_radius_v = int(face_height * 0.15)

        left_cheek_pos = landmarks[self.left_cheek_center]
        right_cheek_pos = landmarks[self.right_cheek_center]

        cv2.ellipse(mask, left_cheek_pos, (cheek_radius_h, cheek_radius_v),
                   0, 0, 360, 255, -1)
        cv2.ellipse(mask, right_cheek_pos, (cheek_radius_h, cheek_radius_v),
                   0, 0, 360, 255, -1)

        mask = cv2.GaussianBlur(mask, (51, 51), 30)

        return mask

    def create_eye_masks(self, landmarks, shape):
        """
        Create eye masks (left and right combined)
        These are used for exclusion zones in smoothing

        Args:
            landmarks: List of (x, y) coordinates
            shape: Image shape

        Returns:
            Binary mask of eye regions
        """
        mask = np.zeros(shape[:2], dtype=np.uint8)

        left_eye_points = np.array([landmarks[i] for i in self.left_eye], dtype=np.int32)
        right_eye_points = np.array([landmarks[i] for i in self.right_eye], dtype=np.int32)

        cv2.fillPoly(mask, [left_eye_points], 255)
        cv2.fillPoly(mask, [right_eye_points], 255)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        mask = cv2.dilate(mask, kernel, iterations=1)

        return mask
