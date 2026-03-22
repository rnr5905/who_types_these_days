#!/usr/bin/env python3
"""
Voice Dictation - Real-time speech-to-text.

USAGE:
    python main.py              # Start the recorder
    python main.py --trigger    # Toggle recording
    python main.py --help       # Show help
"""

import os
import sys
import signal
import time

from config import STT_BACKEND, MAX_RECORDING_SECONDS, COOLDOWN_SECONDS, LONG_RECORDING_THRESHOLD
from stt import get_backend
from recorder import VoiceRecorder
from utils import (
    TRIGGER_FILE, PID_FILE, SYSTEM,
    type_text, trigger,
    supports_signal_trigger
)


# Global state
recorder = None
recording = False
processing = False
cooldown_until = 0
recording_start_time = None


def stop_and_process():
    """Stop recording, transcribe, and output text."""
    global processing, cooldown_until

    try:
        text = recorder.stop()
        duration = recorder.last_duration

        if duration > LONG_RECORDING_THRESHOLD:
            cooldown_until = time.time() + COOLDOWN_SECONDS
            print(f"[DEBUG] Cooldown: {COOLDOWN_SECONDS}s")

        if text:
            print(f"Result: {text}")
            type_text(text)
        else:
            print("No speech detected")
    finally:
        # Always reset processing flag
        processing = False
        print("[DEBUG] Ready for next recording")


def toggle():
    """Toggle recording on/off."""
    global recording, processing, recording_start_time

    if time.time() < cooldown_until:
        print(f"[DEBUG] Cooldown: {int(cooldown_until - time.time())}s")
        return

    if processing:
        print("[DEBUG] Processing, please wait")
        return

    if not recording:
        recording = True
        recording_start_time = time.time()
        recorder.start()
    else:
        recording = False
        processing = True
        stop_and_process()


def show_help():
    """Print help."""
    print(__doc__)
    print(f"OS: {SYSTEM}")
    print(f"Backend: {STT_BACKEND}")
    print()
    print("Backends: vosk (local), groq (cloud), deepgram (cloud)")
    print()
    print("Trigger methods:")
    if supports_signal_trigger():
        print(f"  Signal: SIGUSR1 (instant)")
    print(f"  File: {TRIGGER_FILE}")


def main():
    global recorder, recording, processing, recording_start_time

    # CLI args
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("--help", "-h"):
            show_help()
            return
        elif arg == "--trigger":
            trigger()
            print("Triggered!")
            return
        elif arg == "--status":
            print(f"Running: {PID_FILE.exists()}")
            return

    # Initialize
    print(f"OS: {SYSTEM}")
    print(f"Backend: {STT_BACKEND}")

    backend = get_backend(STT_BACKEND)
    backend.init()

    recorder = VoiceRecorder(backend)

    # Write PID
    PID_FILE.write_text(str(os.getpid()))

    # Setup signal handler (Linux/macOS)
    if supports_signal_trigger():
        signal.signal(signal.SIGUSR1, lambda s, f: toggle())

    print()
    print("=" * 50)
    print(f"Ready! Backend: {backend.name}")
    print()
    print("Toggle: python main.py --trigger")
    if supports_signal_trigger():
        print(f"      : kill -SIGUSR1 $(cat {PID_FILE})")
    print("Quit: Ctrl+C")
    print("=" * 50)

    last_check = 0

    try:
        while True:
            time.sleep(0.1)

            # Check trigger file (fallback for all OS)
            if time.time() - last_check > 0.2:
                last_check = time.time()
                if TRIGGER_FILE.exists():
                    TRIGGER_FILE.unlink()
                    toggle()

            # Auto-stop
            if recording and not processing and recording_start_time:
                if time.time() - recording_start_time >= MAX_RECORDING_SECONDS:
                    print(f"[DEBUG] Auto-stop")
                    recording = False
                    processing = True
                    stop_and_process()

    except KeyboardInterrupt:
        print("\nQuitting...")
    finally:
        PID_FILE.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
