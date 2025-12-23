"""
Main image processing pipeline
"""
from ..effects.blemish_removal import remove_multiple_blemishes
from ..effects.smoothing import smooth_face
from ..effects.makeup import apply_lipstick, apply_blush
from ..effects.sharpening import sharpen_region, create_eyebrow_eyelash_mask


def apply_all_effects(image_manager, slider_values):
    """
    Main processing pipeline - called whenever sliders change

    Order of operations (IMPORTANT):
    1. Start with original image (always)
    2. Remove blemishes (if any)
    3. Apply face smoothing
    4. Apply makeup (lipstick and blush)
    5. Apply sharpening (eyebrow/eyelash)

    Args:
        image_manager: ImageManager instance
        slider_values: {
            'smoothing': 0-100,
            'lipstick': 0-100,
            'blush': 0-100,
            'sharpening': 0-100
        }

    Returns:
        Processed image
    """
    img = image_manager.get_original().copy()

    if image_manager.blemish_points:
        img = remove_multiple_blemishes(img, image_manager.blemish_points)

    if slider_values['smoothing'] > 0:
        img = smooth_face(
            img,
            image_manager.face_masks['face'],
            image_manager.face_masks['eyes'],
            slider_values['smoothing']
        )

    if slider_values['lipstick'] > 0:
        lipstick_color = slider_values.get('lipstick_color', 'red')
        img = apply_lipstick(
            img,
            image_manager.face_masks['lips'],
            lipstick_color,
            slider_values['lipstick']
        )

    if slider_values['blush'] > 0:
        blush_color = slider_values.get('blush_color', 'pink')
        img = apply_blush(
            img,
            image_manager.face_masks['cheeks'],
            slider_values['blush'],
            blush_color
        )

    if slider_values['sharpening'] > 0:
        sharpen_mask = create_eyebrow_eyelash_mask(
            image_manager.face_landmarks,
            img.shape
        )
        img = sharpen_region(img, sharpen_mask, slider_values['sharpening'])

    image_manager.update_working(img)

    return img
