"""GUI overlay for recording status."""

import tkinter as tk

from config import SYSTEM


class Overlay:
    """
    Small overlay window showing recording status.
    Appears at top-center of screen.
    """

    COLORS = {
        "recording": "#ff5f56",   # Red
        "processing": "#ffbd2e",  # Yellow
        "success": "#27c93f",     # Green
    }

    def __init__(self):
        self.root = None

    def show(self, text: str = "Recording...", status: str = "recording") -> None:
        """Show overlay with status text."""
        if self.root:
            self.root.destroy()

        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#1a1a1a")

        # macOS specific window styling
        if SYSTEM == "Darwin":
            self.root.call(
                "::tk::unsupported::MacWindowStyle",
                "style", self.root._w,
                "floating", "closeBox collapseBox resizable"
            )

        frame = tk.Frame(self.root, bg="#1a1a1a", padx=20, pady=15)
        frame.pack()

        color = self.COLORS.get(status, self.COLORS["recording"])
        label = tk.Label(
            frame,
            text=f"● {text}",
            fg=color,
            bg="#1a1a1a",
            font=("Sans", 14, "bold")
        )
        label.pack()

        # Center at top of screen
        self.root.update_idletasks()
        w = self.root.winfo_width()
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"+{(sw-w)//2}+80")
        self.root.update()

    def hide(self) -> None:
        """Hide and destroy overlay."""
        if self.root:
            self.root.destroy()
            self.root = None
