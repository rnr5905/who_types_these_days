"""Deepgram Nova-2 - Fastest cloud transcription."""

import os
import tempfile
import wave

import numpy as np

from .base import STTBackend
from config import SAMPLE_RATE, CHANNELS, DEEPGRAM_API_KEY


class DeepgramBackend(STTBackend):
    """
    Deepgram Nova-2 - Fastest cloud transcription.
    Get free API key ($200 credit) at: https://console.deepgram.com
    """

    def __init__(self):
        self.api_key = DEEPGRAM_API_KEY

    @property
    def name(self) -> str:
        return "Deepgram (cloud)"

    def init(self) -> None:
        if not self.api_key:
            raise ValueError(
                "DEEPGRAM_API_KEY not set!\n"
                "Get free key at https://console.deepgram.com"
            )
        print("Deepgram ready!")

    def transcribe(self, audio: np.ndarray) -> str:
        import requests

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
            with wave.open(f, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(2)
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(audio.tobytes())

        try:
            with open(temp_path, "rb") as f:
                response = requests.post(
                    "https://api.deepgram.com/v1/listen",
                    params={"model": "nova-2", "smart_format": "true", "language": "en"},
                    headers={
                        "Authorization": f"Token {self.api_key}",
                        "Content-Type": "audio/wav"
                    },
                    data=f
                )
            response.raise_for_status()
            result = response.json()
            return result["results"]["channels"][0]["alternatives"][0]["transcript"].strip()
        finally:
            os.unlink(temp_path)
