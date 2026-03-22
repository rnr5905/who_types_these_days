"""Vosk - Local, offline speech recognition."""

import json
import zipfile
from pathlib import Path

import numpy as np
import urllib.request

from .base import STTBackend
from config import SAMPLE_RATE


class VoskBackend(STTBackend):
    """
    Vosk - Local, offline speech recognition.
    No API key required. Model downloaded on first use (~50MB).
    """

    MODEL_NAME = "vosk-model-small-en-us-0.15"

    def __init__(self):
        self.model = None

    @property
    def name(self) -> str:
        return "Vosk (local)"

    @property
    def is_local(self) -> bool:
        return True

    def init(self) -> None:
        from vosk import Model, SetLogLevel
        SetLogLevel(-1)

        model_path = Path.home() / ".vosk" / self.MODEL_NAME

        if not model_path.exists():
            print("Downloading Vosk model...")
            self._download_model()

        self.model = Model(str(model_path))
        print("Vosk ready!")

    def _download_model(self) -> None:
        model_dir = Path.home() / ".vosk"
        model_dir.mkdir(parents=True, exist_ok=True)

        url = f"https://alphacephei.com/vosk/models/{self.MODEL_NAME}.zip"
        zip_path = model_dir / f"{self.MODEL_NAME}.zip"

        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(model_dir)
        zip_path.unlink()
        print("Model downloaded!")

    def transcribe(self, audio: np.ndarray) -> str:
        from vosk import KaldiRecognizer

        rec = KaldiRecognizer(self.model, SAMPLE_RATE)
        for i in range(0, len(audio), 4000):
            rec.AcceptWaveform(audio[i:i+4000].tobytes())

        result = json.loads(rec.FinalResult())
        return result.get("text", "").strip()
