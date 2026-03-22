from .platform import (
    SYSTEM, TEMP_DIR, TRIGGER_FILE, PID_FILE,
    get_system, is_linux, is_macos, is_windows,
    supports_signal_trigger, send_trigger_signal,
    create_trigger_file, trigger
)
from .typing import type_text
