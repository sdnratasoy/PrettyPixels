"""
Sharpening effect using unsharp masking
"""
import cv2
import numpy as np
from ..utils.constants import LEFT_EYEBROW_INDICES, RIGHT_EYEBROW_INDICES
from ..utils.config import SHARPEN_MIN_AMOUNT, SHARPEN_MAX_AMOUNT


def sharpen_region(image, region_mask, intensity=50):
    """
    Apply unsharp masking to sharpen specific regions

    Args:
        image: Input image (BGR)
        region_mask: Binary mask of region to sharpen
        intensity: 0-100

    Returns:
        Sharpened image
    """
    if intensity == 0:
        return image

    blurred = cv2.GaussianBlur(image, (0, 0), 3)

    amount = SHARPEN_MIN_AMOUNT + (intensity / 100.0) * (SHARPEN_MAX_AMOUNT - SHARPEN_MIN_AMOUNT)
    sharpened = cv2.addWeighted(image, 1 + amount, blurred, -amount, 0)

    region_mask_3ch = cv2.cvtColor(region_mask, cv2.COLOR_GRAY2BGR) / 255.0
    result = (sharpened * region_mask_3ch +
              image * (1 - region_mask_3ch))

    return result.astype(np.uint8)


def create_eyebrow_eyelash_mask(landmarks, shape):
    """
    Create mask for eyebrow and eyelash regions

    Args:
        landmarks: List of (x, y) coordinates
        shape: Image shape

    Returns:
        Binary mask of eyebrow/eyelash regions
    """
    mask = np.zeros(shape[:2], dtype=np.uint8)

    left_brow = np.array([landmarks[i] for i in LEFT_EYEBROW_INDICES], dtype=np.int32)
    right_brow = np.array([landmarks[i] for i in RIGHT_EYEBROW_INDICES], dtype=np.int32)

    cv2.fillPoly(mask, [left_brow], 255)
    cv2.fillPoly(mask, [right_brow], 255)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask = cv2.dilate(mask, kernel, iterations=1)

    return mask
