"""
Canvas for displaying before/after images
"""
import tkinter as tk
from ..utils.config import CANVAS_WIDTH, CANVAS_HEIGHT
from ..utils.image_utils import cv2_to_photoimage


class ImageCanvas:
    """Custom canvas for before/after image display"""

    def __init__(self, parent):
        """
        Initialize image canvas with Pretty Pixels styling

        Args:
            parent: Parent Tkinter widget
        """
        bg_color = '#F8F5FA'         # Very light lavender background
        canvas_bg = '#FFFFFF'        # White for canvas
        label_bg = '#E8D5F2'         # Light lavender for labels
        text_color = '#6B5B7E'       # Deep purple-gray
        border_color = '#D4B8E8'     # Medium purple for borders

        self.frame = tk.Frame(parent, bg=bg_color)

        before_frame = tk.Frame(self.frame, bg=label_bg, relief='groove', bd=3,
                               highlightbackground=border_color, highlightthickness=2)
        before_frame.pack(side='left', padx=15, pady=10)

        tk.Label(
            before_frame,
            text='📷 BEFORE',
            font=('Segoe UI', 12, 'bold'),
            bg=label_bg,
            fg=text_color,
            pady=8
        ).pack()

        canvas_container = tk.Frame(before_frame, bg=border_color, padx=3, pady=3,
                                   relief='ridge', bd=2)
        canvas_container.pack(padx=5, pady=5)

        self.before_canvas = tk.Canvas(
            canvas_container,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=canvas_bg,
            highlightthickness=0,
            relief='flat'
        )
        self.before_canvas.pack()

        after_frame = tk.Frame(self.frame, bg=label_bg, relief='groove', bd=3,
                              highlightbackground=border_color, highlightthickness=2)
        after_frame.pack(side='left', padx=15, pady=10)

        tk.Label(
            after_frame,
            text='✨ AFTER',
            font=('Segoe UI', 12, 'bold'),
            bg=label_bg,
            fg=text_color,
            pady=8
        ).pack()

        canvas_container2 = tk.Frame(after_frame, bg=border_color, padx=3, pady=3,
                                    relief='ridge', bd=2)
        canvas_container2.pack(padx=5, pady=5)

        self.after_canvas = tk.Canvas(
            canvas_container2,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg=canvas_bg,
            highlightthickness=0,
            relief='flat'
        )
        self.after_canvas.pack()

    def display_images(self, before_img, after_img):
        """
        Display before and after images

        Args:
            before_img: OpenCV BGR image (before)
            after_img: OpenCV BGR image (after)
        """
        before_photo = cv2_to_photoimage(before_img, CANVAS_WIDTH, CANVAS_HEIGHT)
        after_photo = cv2_to_photoimage(after_img, CANVAS_WIDTH, CANVAS_HEIGHT)

        self.before_canvas.delete('all')
        self.after_canvas.delete('all')

        self.before_canvas.create_image(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2,
            image=before_photo
        )
        self.after_canvas.create_image(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2,
            image=after_photo
        )

        self.before_canvas.image = before_photo
        self.after_canvas.image = after_photo

    def clear(self):
        """Clear both canvases"""
        self.before_canvas.delete('all')
        self.after_canvas.delete('all')
