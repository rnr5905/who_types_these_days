"""Configuration loader and settings."""

import os
from pathlib import Path


def load_env():
    """Load environment variables from .env file."""
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())


load_env()

# Audio settings
SAMPLE_RATE = int(os.environ.get("SAMPLE_RATE", 16000))
CHANNELS = 1

# STT backend
STT_BACKEND = os.environ.get("STT_BACKEND", "vosk")

# Recording limits
MAX_RECORDING_SECONDS = int(os.environ.get("MAX_RECORDING_SECONDS", 120))
COOLDOWN_SECONDS = int(os.environ.get("COOLDOWN_SECONDS", 3))
LONG_RECORDING_THRESHOLD = int(os.environ.get("LONG_RECORDING_THRESHOLD", 60))

# API keys
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
DEEPGRAM_API_KEY = os.environ.get("DEEPGRAM_API_KEY", "")
