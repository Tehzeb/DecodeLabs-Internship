"""
tts_service.py
----------------
Offline text-to-speech using pyttsx3 (wraps SAPI5 on Windows, so no
internet or API key is required). Used to read recognized OCR text
aloud from the UI.

pyttsx3's engine is not safely reusable across threads/requests in
all backends, so each call creates and disposes a fresh engine
instance -- slightly slower, but reliable inside a web server.
"""

from __future__ import annotations

import uuid

import pyttsx3

from backend import config


def synthesize_speech(text: str) -> str:
    """
    Synthesize `text` to a WAV file on disk and return its path.
    Caller is responsible for cleaning up the temp file after serving it.
    """
    if not text or not text.strip():
        raise ValueError("No text provided for speech synthesis.")

    out_path = config.TEMP_DIR / f"tts_{uuid.uuid4().hex}.wav"

    engine = pyttsx3.init()
    try:
        engine.setProperty("rate", config.TTS_RATE)
        engine.setProperty("volume", config.TTS_VOLUME)
        engine.save_to_file(text, str(out_path))
        engine.runAndWait()
    finally:
        engine.stop()

    return str(out_path)
