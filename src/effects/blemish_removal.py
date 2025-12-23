"""
Blemish removal using inpainting
"""
import cv2
import numpy as np
from ..utils.config import BLEMISH_RADIUS, INPAINT_RADIUS


def remove_blemish(image, x, y, radius=BLEMISH_RADIUS):
    """
    Remove blemish at (x, y) using inpainting

    Args:
        image: Input image (BGR)
        x, y: Blemish center coordinates
        radius: Inpainting radius

    Returns:
        Inpainted image
    """
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (x, y), radius, 255, -1)

    result = cv2.inpaint(image, mask, INPAINT_RADIUS, cv2.INPAINT_TELEA)

    return result


def remove_multiple_blemishes(image, blemish_points, radius=BLEMISH_RADIUS):
    """
    Remove multiple blemishes sequentially

    Args:
        image: Input image (BGR)
        blemish_points: List of (x, y) coordinates
        radius: Inpainting radius

    Returns:
        Image with all blemishes removed
    """
    result = image.copy()

    for x, y in blemish_points:
        result = remove_blemish(result, x, y, radius)

    return result
