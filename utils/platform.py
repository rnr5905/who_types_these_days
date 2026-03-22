"""Platform detection and OS-specific utilities."""

import os
import signal
import platform
import tempfile
from pathlib import Path


SYSTEM = platform.system()  # "Linux", "Darwin" (macOS), "Windows"
TEMP_DIR = Path(tempfile.gettempdir())
TRIGGER_FILE = TEMP_DIR / "voice_dictation_trigger"
PID_FILE = TEMP_DIR / "voice_dictation.pid"


def get_system() -> str:
    return SYSTEM


def is_linux() -> bool:
    return SYSTEM == "Linux"


def is_macos() -> bool:
    return SYSTEM == "Darwin"


def is_windows() -> bool:
    return SYSTEM == "Windows"


def supports_signal_trigger() -> bool:
    """Check if OS supports SIGUSR1 for instant triggering."""
    return SYSTEM in ("Linux", "Darwin")


def send_trigger_signal():
    """Send SIGUSR1 to running process (Linux/macOS only)."""
    if not supports_signal_trigger():
        return False

    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            os.kill(pid, signal.SIGUSR1)
            return True
        except (ValueError, ProcessLookupError, PermissionError):
            pass
    return False


def create_trigger_file():
    """Create trigger file (works on all OS)."""
    TRIGGER_FILE.touch()


def trigger():
    """Trigger recording using best method for OS."""
    if supports_signal_trigger():
        # Try signal first (instant), fall back to file
        if not send_trigger_signal():
            create_trigger_file()
    else:
        create_trigger_file()
