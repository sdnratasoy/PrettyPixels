"""
Makeup effects: lipstick and blush
"""
import cv2
import numpy as np
from ..utils.constants import LIPSTICK_RED, LIPSTICK_PINK, BLUSH_PINK
from ..utils.image_utils import feather_mask


def apply_lipstick(image, lip_mask, color='red', intensity=50):
    """
    Apply lipstick color to lips with enhanced visibility

    Args:
        image: Input image (BGR)
        lip_mask: Binary mask of lip region
        color: 'red', 'pink', 'coral', 'berry', 'nude', or RGB tuple (B,G,R)
        intensity: 0-100

    Returns:
        Image with lipstick applied
    """
    if intensity == 0:
        return image

    colors = {
        'red': (0, 0, 200),           # Classic red
        'pink': (180, 100, 255),      # Bright pink
        'coral': (80, 127, 255),      # Coral
        'berry': (128, 0, 128),       # Berry/purple
        'nude': (120, 140, 180),      # Nude/beige
        'wine': (80, 30, 139),        # Wine/dark red
        'orange': (0, 140, 255),      # Orange
        'mauve': (170, 120, 200)      # Mauve
    }

    if isinstance(color, tuple):
        lip_color = np.array(color, dtype=np.float32)
    else:
        lip_color = np.array(colors.get(color, colors['red']), dtype=np.float32)

    lip_mask_feathered = feather_mask(lip_mask, kernel_size=5)
    lip_mask_3ch = cv2.cvtColor(lip_mask_feathered, cv2.COLOR_GRAY2BGR) / 255.0

    image_float = image.astype(np.float32)

    alpha = min(intensity / 100.0 * 1.5, 1.0)  

    hsv = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = hsv[:, :, 1] * (1 + 0.3 * lip_mask_feathered / 255.0)  # Boost saturation
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    saturated = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    overlay = np.zeros_like(image_float)
    overlay[:] = lip_color

    mask_bool = saturated < 128
    blended = saturated.copy()
    blended[mask_bool] = (2 * saturated[mask_bool] * overlay[mask_bool]) / 255.0
    blended[~mask_bool] = 255 - 2 * (255 - saturated[~mask_bool]) * (255 - overlay[~mask_bool]) / 255.0

    result = image_float * (1 - lip_mask_3ch * alpha) + blended * lip_mask_3ch * alpha

    return np.clip(result, 0, 255).astype(np.uint8)


def apply_blush(image, cheek_masks, intensity=50, color='pink'):
    """
    Apply blush to cheeks with enhanced visibility

    Args:
        image: Input image (BGR)
        cheek_masks: Binary mask of cheek regions
        intensity: 0-100
        color: 'pink', 'peach', 'coral', 'rose', 'bronze', or RGB tuple (B,G,R)

    Returns:
        Image with blush applied
    """
    if intensity == 0:
        return image

    colors = {
        'pink': (180, 100, 255),      # Bright pink
        'peach': (140, 180, 255),     # Peach
        'coral': (100, 140, 255),     # Coral
        'rose': (150, 100, 200),      # Rose
        'bronze': (80, 120, 180),     # Bronze/terracotta
        'mauve': (180, 130, 200)      # Mauve
    }

    if isinstance(color, tuple):
        blush_color = np.array(color, dtype=np.float32)
    else:
        blush_color = np.array(colors.get(color, colors['pink']), dtype=np.float32)

    overlay = np.zeros_like(image, dtype=np.float32)
    overlay[:] = blush_color

    cheek_mask_3ch = cv2.cvtColor(cheek_masks, cv2.COLOR_GRAY2BGR) / 255.0


    alpha = min(intensity / 100.0 * 1.0, 1.0)
    image_float = image.astype(np.float32)

    hsv = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_BGR2HSV).astype(np.float32)
    cheek_mask_normalized = cheek_masks / 255.0
    hsv[:, :, 1] = hsv[:, :, 1] * (1 + 0.2 * cheek_mask_normalized)  
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    saturated = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

    mask_bool = saturated < 128
    blended = saturated.copy()
    blended[mask_bool] = (2 * saturated[mask_bool] * overlay[mask_bool]) / 255.0
    blended[~mask_bool] = 255 - 2 * (255 - saturated[~mask_bool]) * (255 - overlay[~mask_bool]) / 255.0

    result = image_float * (1 - cheek_mask_3ch * alpha) + blended * cheek_mask_3ch * alpha

    return np.clip(result, 0, 255).astype(np.uint8)
