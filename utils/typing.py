"""Cross-platform text output - uses best method for each OS."""

import subprocess
import platform

# Detect OS directly (avoid circular import)
SYSTEM = platform.system()

# Try to import cross-platform fallbacks
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False


def type_text(text: str) -> None:
    """
    Type text and copy to clipboard.
    Uses OS-specific best method.
    """
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
    type_with_best_method(text)


def copy_to_clipboard(text: str) -> None:
    """Copy text to clipboard using best method for OS."""
    if SYSTEM == "Linux":
        # xclip is faster on Linux
        try:
            subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=text.encode(),
                check=True,
                capture_output=True
            )
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    # Fallback to pyperclip (macOS, Windows, or if xclip fails)
    if HAS_PYPERCLIP:
        try:
            pyperclip.copy(text)
            return
        except Exception:
            pass

    print("Warning: Clipboard not available")


def type_with_best_method(text: str) -> None:
    """Type text using best method for OS."""
    if SYSTEM == "Linux":
        # xdotool is faster and more reliable on Linux
        try:
            subprocess.run(
                ["xdotool", "type", "--clearmodifiers", text],
                check=True,
                capture_output=True
            )
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

    # Fallback to pyautogui (macOS, Windows)
    if HAS_PYAUTOGUI:
        try:
            pyautogui.write(text, interval=0.01)
            return
        except Exception as e:
            print(f"Type error: {e}")
    else:
        print("Warning: Install pyautogui for typing support")
