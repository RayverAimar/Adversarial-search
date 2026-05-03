"""Shared colors, fonts, and helpers for the Tk UI."""

BG = "#1e1e2e"
SURFACE = "#2a2a3e"
SURFACE_LIGHT = "#3b3b54"
TEXT = "#e0e0e0"
TEXT_DIM = "#a0a0a0"
BORDER = "#45475a"

ACCENT_X = "#ff6b9d"
ACCENT_O = "#6bcefa"

PRIMARY = "#89b4fa"
PRIMARY_HOVER = "#b4befe"
SUCCESS = "#a6e3a1"
WARNING = "#fab387"
ERROR = "#f38ba8"

FONT_TITLE = ("Helvetica", 24, "bold")
FONT_HEADING = ("Helvetica", 15, "bold")
FONT_BODY = ("Helvetica", 12)
FONT_BODY_BOLD = ("Helvetica", 12, "bold")
FONT_SMALL = ("Helvetica", 10)
FONT_BUTTON = ("Helvetica", 13, "bold")
FONT_MONO = ("Menlo", 11)
FONT_BOARD = ("Helvetica", 32, "bold")
FONT_STATUS = ("Helvetica", 18, "bold")


def center(window, width: int, height: int) -> None:
    """Resize ``window`` to ``width x height`` and center it on the screen."""
    window.update_idletasks()
    sw = window.winfo_screenwidth()
    sh = window.winfo_screenheight()
    x = max(0, (sw - width) // 2)
    y = max(0, (sh - height) // 3)
    window.geometry(f"{width}x{height}+{x}+{y}")
