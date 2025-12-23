"""
Main application window and controller
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np

from ..utils.config import (
    WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT,
    CANVAS_WIDTH, CANVAS_HEIGHT, SUPPORTED_FORMATS
)
from ..processing.face_detector import FaceDetector
from ..processing.mask_generator import MaskGenerator
from ..processing.image_manager import ImageManager
from ..processing.filters import apply_all_effects
from .image_canvas import ImageCanvas
from .control_panel import ControlPanel
from .event_handlers import EventHandlers


class MainWindow:
    """Main application controller"""

    def __init__(self, root):
        """
        Initialize main window

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

        self.image_manager = ImageManager()
        self.face_detector = FaceDetector()
        self.mask_generator = MaskGenerator()

        self.setup_layout()

    def setup_layout(self):
        """Setup GUI layout with Pretty Pixels branding"""
        bg_gradient_top = '#E8D5F2'      # Light lavender
        bg_gradient_bottom = '#D5E8F2'   # Light blue
        accent_purple = '#B8A4D4'        # Soft purple
        accent_pink = '#F4C4D8'          # Soft pink
        button_bg = '#E0CEF5'            # Light purple
        button_hover = '#D4B8E8'         # Medium purple
        text_color = '#6B5B7E'           # Deep purple-gray

        self.root.configure(bg=bg_gradient_top)

        header_frame = tk.Frame(self.root, bg=bg_gradient_top, height=80)
        header_frame.pack(side='top', fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)

        logo_frame = tk.Frame(header_frame, bg=bg_gradient_top)
        logo_frame.pack(side='left', padx=20, pady=10)

        try:
            from PIL import Image, ImageTk
            logo_path = 'assets/logo.png'
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((60, 60), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(logo_frame, image=logo_photo, bg=bg_gradient_top)
            logo_label.image = logo_photo  # Keep reference
            logo_label.pack(side='left')
        except:
            tk.Label(
                logo_frame,
                text='✨',
                font=('Arial', 36),
                bg=bg_gradient_top,
                fg=accent_purple
            ).pack(side='left')

        tk.Label(
            logo_frame,
            text='Pretty Pixels',
            font=('Segoe UI', 20, 'bold'),
            bg=bg_gradient_top,
            fg=text_color
        ).pack(side='left', padx=10)

        tk.Label(
            logo_frame,
            text='Face Editor',
            font=('Segoe UI', 11),
            bg=bg_gradient_top,
            fg=accent_purple
        ).pack(side='left')

        button_frame = tk.Frame(header_frame, bg=bg_gradient_top)
        button_frame.pack(side='right', padx=20, pady=10)

        button_style = {
            'font': ('Segoe UI', 10, 'bold'),
            'bg': button_bg,
            'fg': text_color,
            'activebackground': button_hover,
            'activeforeground': text_color,
            'relief': 'raised',
            'bd': 2,
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2',
            'borderwidth': 1,
            'highlightbackground': accent_purple,
            'highlightthickness': 1
        }

        for btn_text, btn_command in [
            ('📁 Load Image', self.load_image),
            ('💾 Save Image', self.save_image),
            ('🔄 Reset', self.reset_image)
        ]:
            btn_container = tk.Frame(button_frame, bg=bg_gradient_top, highlightthickness=0)
            btn_container.pack(side='left', padx=5)

            btn = tk.Button(
                btn_container,
                text=btn_text,
                command=btn_command,
                **button_style
            )
            btn.pack()

        canvas_container = tk.Frame(self.root, bg='#F8F5FA')
        canvas_container.pack(side='top', fill='both', expand=True, pady=10)

        self.canvas = ImageCanvas(canvas_container)
        self.canvas.frame.pack(expand=True)  # Center the canvas

        self.control_panel = ControlPanel(self.root, self.on_slider_change)
        self.control_panel.frame.pack(side='bottom', fill='both', padx=20, pady=10)

        self.event_handler = EventHandlers(self.canvas, self.on_canvas_click)

    def load_image(self):
        """Load image from file"""
        path = filedialog.askopenfilename(filetypes=SUPPORTED_FORMATS)
        if not path:
            return

        try:
            with open(path, 'rb') as f:
                file_bytes = np.frombuffer(f.read(), dtype=np.uint8)
                img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if img is None or not isinstance(img, np.ndarray):
                messagebox.showerror("Error", "Failed to load image")
                return

            landmarks = self.face_detector.detect(img)
            if landmarks is None:
                messagebox.showerror("Error", "No face detected in image")
                return

            masks = self.mask_generator.generate_all_masks(landmarks, img.shape)

            self.image_manager.original_image = img.copy()
            self.image_manager.working_image = img.copy()
            self.image_manager.blemish_points = []
            self.image_manager.set_face_data(landmarks, masks)

            self.update_display()

            self.control_panel.reset_values()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {str(e)}")

    def save_image(self):
        """Save processed image"""
        if self.image_manager.working_image is None:
            messagebox.showwarning("Warning", "No image to save")
            return

        path = filedialog.asksaveasfilename(
            defaultextension='.jpg',
            filetypes=[
                ('JPEG files', '*.jpg'),
                ('PNG files', '*.png')
            ]
        )

        if path:
            try:
                cv2.imwrite(path, self.image_manager.working_image)
                messagebox.showinfo("Success", "Image saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    def reset_image(self):
        """Reset all effects"""
        if self.image_manager.original_image is None:
            return

        self.image_manager.reset()
        self.control_panel.reset_values()
        self.update_display()

    def on_slider_change(self):
        """Handle slider change with debouncing"""
        if self.image_manager.original_image is None:
            return

        if hasattr(self, '_slider_timer'):
            self.root.after_cancel(self._slider_timer)
        self._slider_timer = self.root.after(100, self.apply_effects)

    def apply_effects(self):
        """Apply all effects based on slider values"""
        if self.image_manager.original_image is None:
            return

        try:
            slider_values = self.control_panel.get_values()

            apply_all_effects(self.image_manager, slider_values)

            self.update_display()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply effects: {str(e)}")

    def on_canvas_click(self, canvas_x, canvas_y):
        """
        Handle click on canvas for blemish removal

        Args:
            canvas_x: Canvas X coordinate
            canvas_y: Canvas Y coordinate
        """
        if self.image_manager.original_image is None:
            return

        try:
            img_x, img_y = self.canvas_to_image_coords(canvas_x, canvas_y)

            self.image_manager.add_blemish_point(img_x, img_y)

            self.apply_effects()

            self.canvas.after_canvas.create_oval(
                canvas_x - 5, canvas_y - 5,
                canvas_x + 5, canvas_y + 5,
                outline='red',
                width=2
            )

        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove blemish: {str(e)}")

    def canvas_to_image_coords(self, canvas_x, canvas_y):
        """
        Convert canvas coordinates to image coordinates

        Args:
            canvas_x: Canvas X coordinate
            canvas_y: Canvas Y coordinate

        Returns:
            Tuple of (img_x, img_y) image coordinates
        """
        img_h, img_w = self.image_manager.original_image.shape[:2]

        scale = min(CANVAS_WIDTH / img_w, CANVAS_HEIGHT / img_h)

        display_w = int(img_w * scale)
        display_h = int(img_h * scale)

        offset_x = (CANVAS_WIDTH - display_w) // 2
        offset_y = (CANVAS_HEIGHT - display_h) // 2

        img_x = int((canvas_x - offset_x) / scale)
        img_y = int((canvas_y - offset_y) / scale)

        img_x = max(0, min(img_x, img_w - 1))
        img_y = max(0, min(img_y, img_h - 1))

        return img_x, img_y

    def update_display(self):
        """Update before/after image display"""
        before = self.image_manager.get_original()
        after = self.image_manager.working_image if self.image_manager.working_image is not None else before
        self.canvas.display_images(before, after)
