"""Abstract base class for STT backends."""

from abc import ABC, abstractmethod
import numpy as np


class STTBackend(ABC):
    """Abstract base class for speech-to-text backends."""

    @abstractmethod
    def init(self) -> None:
        """Initialize the backend."""
        pass

    @abstractmethod
    def transcribe(self, audio: np.ndarray) -> str:
        """Transcribe audio to text."""
        pass

    @property
    def name(self) -> str:
        return "unknown"

    @property
    def is_local(self) -> bool:
        return False
