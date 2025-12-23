"""
Control panel with sliders and buttons
"""
import tkinter as tk
from ..utils.config import SLIDER_MIN, SLIDER_MAX, SLIDER_DEFAULT


class ControlPanel:
    """Panel with all controls (sliders, buttons)"""

    def __init__(self, parent, on_change_callback):
        """
        Initialize control panel

        Args:
            parent: Parent Tkinter widget
            on_change_callback: Function to call when slider changes
        """
        bg_color = '#F5EFF9'         # Very light lavender
        accent_purple = '#B8A4D4'    # Soft purple
        text_color = '#6B5B7E'       # Deep purple-gray
        slider_bg = '#E8D5F2'        # Light lavender
        slider_active = '#D4B8E8'    # Medium purple

        self.frame = tk.Frame(parent, bg=bg_color, relief='flat', borderwidth=0)
        self.callback = on_change_callback

        title_frame = tk.Frame(self.frame, bg=bg_color)
        title_frame.pack(pady=5)

        tk.Label(
            title_frame,
            text='🎨',
            font=('Arial', 16),
            bg=bg_color
        ).pack(side='left')

        tk.Label(
            title_frame,
            text='EDITING CONTROLS',
            font=('Segoe UI', 14, 'bold'),
            bg=bg_color,
            fg=text_color
        ).pack(side='left', padx=10)

        self.bg_color = bg_color
        self.text_color = text_color

        slider_config = {
            'from_': SLIDER_MIN,
            'to': SLIDER_MAX,
            'orient': 'horizontal',
            'length': 400,
            'bg': bg_color,
            'fg': text_color,
            'troughcolor': slider_bg,
            'activebackground': accent_purple,
            'highlightthickness': 0,
            'font': ('Segoe UI', 9),
            'relief': 'flat'
        }

        controls_grid = tk.Frame(self.frame, bg=bg_color)
        controls_grid.pack(pady=5, padx=40, fill='both', expand=True)

        controls_grid.columnconfigure(0, weight=3, minsize=500)  # Slider column
        controls_grid.columnconfigure(1, weight=0)  # Label column
        controls_grid.columnconfigure(2, weight=0)  # Dropdown column

        slider_config['length'] = 0  # Will expand to fill

        self.smoothing_slider = tk.Scale(
            controls_grid,
            label='✨ Face Smoothing',
            command=lambda v: self.callback(),
            **slider_config
        )
        self.smoothing_slider.set(SLIDER_DEFAULT)
        self.smoothing_slider.grid(row=0, column=0, columnspan=3, sticky='ew', pady=2, padx=5)

        self.lipstick_slider = tk.Scale(
            controls_grid,
            label='💄 Lipstick Intensity',
            command=lambda v: self.callback(),
            **slider_config
        )
        self.lipstick_slider.set(SLIDER_DEFAULT)
        self.lipstick_slider.grid(row=1, column=0, sticky='ew', pady=2, padx=5)

        tk.Label(
            controls_grid,
            text='Color:',
            font=('Segoe UI', 9),
            bg=bg_color,
            fg=text_color
        ).grid(row=1, column=1, padx=(10, 5), sticky='e')

        self.lipstick_color = tk.StringVar(value='red')
        colors = ['red', 'pink', 'coral', 'berry', 'nude', 'wine', 'orange', 'mauve']
        lipstick_menu = tk.OptionMenu(controls_grid, self.lipstick_color, *colors, command=lambda v: self.callback())
        lipstick_menu.config(
            width=8,
            bg=slider_bg,
            fg=text_color,
            activebackground=accent_purple,
            relief='flat',
            font=('Segoe UI', 9),
            highlightthickness=0
        )
        lipstick_menu.grid(row=1, column=2, padx=5, sticky='w')

        self.blush_slider = tk.Scale(
            controls_grid,
            label='🌸 Blush Intensity',
            command=lambda v: self.callback(),
            **slider_config
        )
        self.blush_slider.set(SLIDER_DEFAULT)
        self.blush_slider.grid(row=2, column=0, sticky='ew', pady=2, padx=5)

        tk.Label(
            controls_grid,
            text='Color:',
            font=('Segoe UI', 9),
            bg=bg_color,
            fg=text_color
        ).grid(row=2, column=1, padx=(10, 5), sticky='e')

        self.blush_color = tk.StringVar(value='pink')
        blush_colors = ['pink', 'peach', 'coral', 'rose', 'bronze', 'mauve']
        blush_menu = tk.OptionMenu(controls_grid, self.blush_color, *blush_colors, command=lambda v: self.callback())
        blush_menu.config(
            width=8,
            bg=slider_bg,
            fg=text_color,
            activebackground=accent_purple,
            relief='flat',
            font=('Segoe UI', 9),
            highlightthickness=0
        )
        blush_menu.grid(row=2, column=2, padx=5, sticky='w')

        self.sharpening_slider = tk.Scale(
            controls_grid,
            label='👁️ Eye/Eyebrow Sharpening',
            command=lambda v: self.callback(),
            **slider_config
        )
        self.sharpening_slider.set(SLIDER_DEFAULT)
        self.sharpening_slider.grid(row=3, column=0, columnspan=3, sticky='ew', pady=2, padx=5)

        instructions_frame = tk.Frame(self.frame, bg='#EAE0F5', relief='flat')
        instructions_frame.pack(pady=8, padx=30, fill='x')

        tk.Label(
            instructions_frame,
            text='💡',
            font=('Arial', 14),
            bg='#EAE0F5'
        ).pack(side='left', padx=10, pady=10)

        instructions = (
            "Click on blemishes in the AFTER image to remove them. "
            "Adjust sliders to control effect intensity. "
            "Choose colors from dropdowns for custom looks!"
        )
        tk.Label(
            instructions_frame,
            text=instructions,
            font=('Segoe UI', 9),
            bg='#EAE0F5',
            fg=text_color,
            wraplength=700,
            justify='left'
        ).pack(side='left', pady=10, padx=5)

    def get_values(self):
        """
        Get current slider values

        Returns:
            Dictionary of slider values
        """
        return {
            'smoothing': self.smoothing_slider.get(),
            'lipstick': self.lipstick_slider.get(),
            'lipstick_color': self.lipstick_color.get(),
            'blush': self.blush_slider.get(),
            'blush_color': self.blush_color.get(),
            'sharpening': self.sharpening_slider.get()
        }

    def reset_values(self):
        """Reset all sliders to default"""
        self.smoothing_slider.set(SLIDER_DEFAULT)
        self.lipstick_slider.set(SLIDER_DEFAULT)
        self.blush_slider.set(SLIDER_DEFAULT)
        self.sharpening_slider.set(SLIDER_DEFAULT)
