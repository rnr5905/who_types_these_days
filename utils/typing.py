"""Cross-platform text output."""

import subprocess
from config import SYSTEM


def type_text(text: str) -> None:
    """Type text and copy to clipboard."""
    if not text:
        return

    # Capitalize first letter
    if text[0].islower():
        text = text[0].upper() + text[1:]

    # Add trailing space
    text += " "

    # Copy to clipboard
    copy_to_clipboard(text)

    # Type the text
    type_it(text)


def copy_to_clipboard(text: str) -> None:
    """Copy text to clipboard."""
    if SYSTEM == "Linux":
        subprocess.run(
            ["xclip", "-selection", "clipboard"],
            input=text.encode(),
            check=True
        )
    elif SYSTEM == "Darwin":  # macOS
        subprocess.run(
            ["pbcopy"],
            input=text.encode(),
            check=True
        )
    else:  # Windows
        import pyperclip
        pyperclip.copy(text)


def type_it(text: str) -> None:
    """Type text."""
    if SYSTEM == "Linux":
        subprocess.run(
            ["xdotool", "type", "--clearmodifiers", text],
            check=True
        )
    elif SYSTEM == "Darwin":  # macOS
        subprocess.run(
            ["osascript", "-e", f'tell application "System Events" to keystroke "{text}"'],
            check=True
        )
    else:  # Windows
        import pyautogui
        pyautogui.write(text, interval=0.01)
