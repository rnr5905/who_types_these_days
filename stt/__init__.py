"""STT backend registry."""

from .base import STTBackend
from .vosk import VoskBackend
from .groq import GroqBackend
from .deepgram import DeepgramBackend


BACKENDS = {
    "vosk": VoskBackend,
    "groq": GroqBackend,
    "deepgram": DeepgramBackend,
}


def get_backend(name: str) -> STTBackend:
    """Get STT backend instance by name."""
    if name not in BACKENDS:
        raise ValueError(f"Unknown backend: {name}. Available: {list(BACKENDS.keys())}")
    return BACKENDS[name]()
