"""
digit_service.py
------------------
Inference wrapper around the custom-trained DigitCNN
(backend/models/digit_cnn.py + train_digit_model.py).

Accepts either an uploaded image or a canvas drawing (both arrive as
raw image bytes from the frontend), preprocesses it to match MNIST's
convention (28x28 grayscale, white digit on black background,
normalized), and returns a full probability distribution so the UI
can render an animated confidence bar chart rather than just a
single label.
"""

from __future__ import annotations

import threading
from typing import Optional

import cv2
import numpy as np
import torch

from backend import config
from backend.models.digit_cnn import DigitCNN


class DigitService:
    _instance: Optional["DigitService"] = None
    _lock = threading.Lock()

    def __init__(self):
        self._model: Optional[DigitCNN] = None
        self._model_lock = threading.Lock()
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @classmethod
    def instance(cls) -> "DigitService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = DigitService()
        return cls._instance

    @property
    def is_trained(self) -> bool:
        return config.DIGIT_MODEL_PATH.exists()

    def _get_model(self) -> DigitCNN:
        if self._model is None:
            with self._model_lock:
                if self._model is None:
                    if not self.is_trained:
                        raise FileNotFoundError(
                            "Digit model weights not found. Run "
                            "'python -m backend.models.train_digit_model' first."
                        )
                    model = DigitCNN()
                    state = torch.load(config.DIGIT_MODEL_PATH, map_location=self._device)
                    model.load_state_dict(state)
                    model.to(self._device)
                    model.eval()
                    self._model = model
        return self._model

    @staticmethod
    def _preprocess(img_bgr: np.ndarray) -> torch.Tensor:
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)

        # Auto-invert: MNIST digits are white-on-black. If the image
        # looks like dark ink on a light background (typical of a
        # photographed page or a canvas drawn with a dark pen), flip it.
        if gray.mean() > 127:
            gray = 255 - gray

        # Otsu threshold to clean up anti-aliasing / noise
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        coords = cv2.findNonZero(thresh)
        if coords is not None:
            x, y, w, h = cv2.boundingRect(coords)
            thresh = thresh[y : y + h, x : x + w]

        # pad to square, then resize with margin (MNIST digits aren't edge-to-edge)
        h, w = thresh.shape
        size = max(h, w)
        square = np.zeros((size, size), dtype=np.uint8)
        y_off, x_off = (size - h) // 2, (size - w) // 2
        square[y_off : y_off + h, x_off : x_off + w] = thresh

        margin = int(size * 0.2)
        square = cv2.copyMakeBorder(
            square, margin, margin, margin, margin, cv2.BORDER_CONSTANT, value=0
        )

        resized = cv2.resize(square, (28, 28), interpolation=cv2.INTER_AREA)
        norm = (resized.astype(np.float32) / 255.0 - 0.1307) / 0.3081
        tensor = torch.from_numpy(norm).unsqueeze(0).unsqueeze(0)  # 1x1x28x28
        return tensor

    def predict(self, img_bgr: np.ndarray) -> dict:
        model = self._get_model()
        tensor = self._preprocess(img_bgr).to(self._device)
        probs = model.predict_proba(tensor).squeeze(0).cpu().tolist()

        ranked = sorted(
            [{"digit": i, "probability": round(p, 5)} for i, p in enumerate(probs)],
            key=lambda d: d["probability"],
            reverse=True,
        )
        return {
            "predicted_digit": ranked[0]["digit"],
            "confidence": ranked[0]["probability"],
            "probabilities": ranked,
        }


def get_digit_service() -> DigitService:
    return DigitService.instance()
