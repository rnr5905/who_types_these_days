"""Platform utilities - uses SYSTEM from config."""

import os
import signal
import tempfile
from pathlib import Path

from config import SYSTEM

TEMP_DIR = Path(tempfile.gettempdir())
TRIGGER_FILE = TEMP_DIR / "voice_dictation_trigger"
PID_FILE = TEMP_DIR / "voice_dictation.pid"


def is_linux() -> bool:
    return SYSTEM == "Linux"


def is_macos() -> bool:
    return SYSTEM == "Darwin"


def is_windows() -> bool:
    return SYSTEM == "Windows"


def supports_signal_trigger() -> bool:
    return SYSTEM in ("Linux", "Darwin")


def send_trigger_signal():
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
    TRIGGER_FILE.touch()


def trigger():
    if supports_signal_trigger():
        if not send_trigger_signal():
            create_trigger_file()
    else:
        create_trigger_file()
