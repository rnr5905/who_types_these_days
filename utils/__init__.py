from config import SYSTEM
from utils.platform import (
    TEMP_DIR, TRIGGER_FILE, PID_FILE,
    is_linux, is_macos, is_windows,
    supports_signal_trigger, send_trigger_signal,
    create_trigger_file, trigger
)
from utils.typing import type_text
