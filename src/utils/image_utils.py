"""
Image conversion and utility functions
"""
import cv2
import numpy as np
from PIL import Image, ImageTk


def cv2_to_pil(cv2_image):
    """Convert OpenCV BGR image to PIL RGB image"""
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb_image)


def pil_to_cv2(pil_image):
    """Convert PIL RGB image to OpenCV BGR image"""
    rgb_array = np.array(pil_image)
    return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)


def cv2_to_photoimage(cv2_image, target_width=400, target_height=500):
    """
    Convert OpenCV image to Tkinter PhotoImage with resizing

    Args:
        cv2_image: OpenCV BGR image
        target_width: Target width for display
        target_height: Target height for display

    Returns:
        ImageTk.PhotoImage
    """
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

    h, w = rgb_image.shape[:2]
    scale = min(target_width / w, target_height / h)
    new_w, new_h = int(w * scale), int(h * scale)

    resized = cv2.resize(rgb_image, (new_w, new_h), interpolation=cv2.INTER_AREA)

    pil_image = Image.fromarray(resized)
    return ImageTk.PhotoImage(pil_image)


def feather_mask(mask, kernel_size=15):
    """
    Apply Gaussian blur to mask edges for smooth blending

    Args:
        mask: Binary mask (0-255)
        kernel_size: Blur kernel size (must be odd)

    Returns:
        Feathered mask (0-255)
    """
    if kernel_size % 2 == 0:
        kernel_size += 1

    return cv2.GaussianBlur(mask, (kernel_size, kernel_size), 0)


def blend_images(img1, img2, mask, alpha=1.0):
    """
    Blend two images using mask and alpha

    Args:
        img1: Background image
        img2: Foreground image
        mask: Blending mask (0-255)
        alpha: Overall blend strength (0-1)

    Returns:
        Blended image
    """
    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) / 255.0
    mask_3ch = mask_3ch * alpha

    result = img2 * mask_3ch + img1 * (1 - mask_3ch)
    return result.astype(np.uint8)
