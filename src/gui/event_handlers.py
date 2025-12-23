"""
Mouse event handlers for interactive tools
"""


class EventHandlers:
    """Mouse event handlers for interactive tools"""

    def __init__(self, canvas, click_callback):
        """
        Initialize event handlers

        Args:
            canvas: ImageCanvas instance
            click_callback: Function to call on click with (x, y) coordinates
        """
        self.canvas = canvas
        self.callback = click_callback

        canvas.after_canvas.bind('<Button-1>', self.on_canvas_click)

    def on_canvas_click(self, event):
        """
        Handle click on after canvas for blemish removal

        Args:
            event: Tkinter event object
        """
        canvas_x = event.x
        canvas_y = event.y

        self.callback(canvas_x, canvas_y)
