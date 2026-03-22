"""Voice recorder with audio capture and transcription."""

import numpy as np
import sounddevice as sd

from config import SAMPLE_RATE, CHANNELS
from overlay import Overlay
from stt import STTBackend


class VoiceRecorder:
    """Handles audio recording and transcription."""

    def __init__(self, backend: STTBackend):
        self.backend = backend
        self.overlay = Overlay()
        self.is_recording = False
        self.audio_data = []
        self.stream = None
        self.last_duration = 0

    def start(self) -> None:
        """Start recording audio."""
        self.audio_data = []
        self.is_recording = True
        self.overlay.show("Recording...", "recording")

        def callback(indata, frames, time_info, status):
            if self.is_recording:
                self.audio_data.append(indata.copy())

        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype='int16',
            callback=callback
        )
        self.stream.start()

    def stop(self) -> str:
        """Stop recording and return transcribed text."""
        self.is_recording = False

        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None

        self.overlay.show("Processing...", "processing")

        text = ""
        if self.audio_data:
            audio = np.concatenate(self.audio_data).flatten()
            self.last_duration = len(audio) / SAMPLE_RATE
            max_amp = np.max(np.abs(audio))
            print(f"[DEBUG] {self.last_duration:.2f}s, amplitude={max_amp}")

            if max_amp > 100:
                try:
                    text = self.backend.transcribe(audio)
                except Exception as e:
                    print(f"Transcription error: {e}")
            else:
                print("[DEBUG] Audio too quiet")

        self.overlay.hide()
        return text
