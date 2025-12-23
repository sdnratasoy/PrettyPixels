"""
Pretty Pixels - Face Editing Application
Main entry point
"""
import tkinter as tk
from src.gui.main_window import MainWindow


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
