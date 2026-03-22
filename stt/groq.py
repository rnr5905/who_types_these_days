"""Groq Whisper API - Fast cloud transcription."""

import os
import sys
import subprocess
import tempfile
import wave

import numpy as np

from .base import STTBackend
from config import SAMPLE_RATE, CHANNELS, GROQ_API_KEY


class GroqBackend(STTBackend):
    """
    Groq Whisper API - Fast cloud transcription.
    Get free API key at: https://console.groq.com
    """

    def __init__(self):
        self.client = None
        self.api_key = GROQ_API_KEY

    @property
    def name(self) -> str:
        return "Groq Whisper (cloud)"

    def init(self) -> None:
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not set!\n"
                "Get free key at https://console.groq.com"
            )

        try:
            from groq import Groq
        except ImportError:
            print("Installing groq...")
            subprocess.run([sys.executable, "-m", "pip", "install", "groq"], check=True)
            from groq import Groq

        self.client = Groq(api_key=self.api_key)
        print("Groq ready!")

    def transcribe(self, audio: np.ndarray) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
            with wave.open(f, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(audio.tobytes())

        try:
            with open(temp_path, "rb") as f:
                return self.client.audio.transcriptions.create(
                    file=f,
                    model="whisper-large-v3-turbo",
                    language="en",
                    response_format="text"
                ).strip()
        finally:
            os.unlink(temp_path)
