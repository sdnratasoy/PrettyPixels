"""
Face smoothing using bilateral filter
"""
import cv2
import numpy as np
from ..utils.config import SMOOTHING_MIN_D, SMOOTHING_MAX_D, SMOOTHING_MIN_SIGMA, SMOOTHING_MAX_SIGMA
from ..utils.image_utils import feather_mask


def smooth_face(image, face_mask, eye_masks, intensity=50):
    """
    Apply bilateral filter smoothing to face, preserving eyes

    Args:
        image: Input image (BGR)
        face_mask: Binary mask of face region
        eye_masks: Binary mask of eye regions to preserve
        intensity: 0-100, controls smoothing strength

    Returns:
        Smoothed image
    """
    if intensity == 0:
        return image

    d = int(SMOOTHING_MIN_D + (intensity / 100) * (SMOOTHING_MAX_D - SMOOTHING_MIN_D))
    sigma_color = int(SMOOTHING_MIN_SIGMA + (intensity / 100) * (SMOOTHING_MAX_SIGMA - SMOOTHING_MIN_SIGMA))
    sigma_space = int(SMOOTHING_MIN_SIGMA + (intensity / 100) * (SMOOTHING_MAX_SIGMA - SMOOTHING_MIN_SIGMA))

    smoothed = cv2.bilateralFilter(image, d, sigma_color, sigma_space)

    smooth_mask = cv2.subtract(face_mask, eye_masks)
    smooth_mask = feather_mask(smooth_mask, kernel_size=15)

    alpha = intensity / 100.0
    smooth_mask_3ch = cv2.cvtColor(smooth_mask, cv2.COLOR_GRAY2BGR) / 255.0

    result = (smoothed * smooth_mask_3ch * alpha +
              image * (1 - smooth_mask_3ch * alpha))

    return result.astype(np.uint8)
