"""
ocr_service.py
----------------
Optical Character Recognition service built on EasyOCR (a deep-learning
based OCR engine using CRAFT text detection + CRNN recognition).

Loaded lazily as a singleton because model initialization is a
noticeable (~seconds) one-time cost; subsequent calls are fast.
"""

from __future__ import annotations

import threading
from typing import Optional

import easyocr

from backend import config
from backend.utils.image_utils import draw_boxes, cv2_to_base64, resize_max_dim


class OCRService:
    _instance: Optional["OCRService"] = None
    _lock = threading.Lock()

    def __init__(self):
        self._reader: Optional[easyocr.Reader] = None
        self._model_lock = threading.Lock()

    @classmethod
    def instance(cls) -> "OCRService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = OCRService()
        return cls._instance

    def _get_reader(self) -> easyocr.Reader:
        if self._reader is None:
            with self._model_lock:
                if self._reader is None:
                    self._reader = easyocr.Reader(
                        config.OCR_LANGUAGES, gpu=config.OCR_GPU
                    )
        return self._reader

    def warm_up(self) -> None:
        """Force model load ahead of the first real request (called at server startup)."""
        self._get_reader()

    @property
    def is_ready(self) -> bool:
        return self._reader is not None

    def recognize(self, img_bgr) -> dict:
        """
        Run OCR on a BGR image.
        Returns dict with: full_text, detections[], annotated_image (base64)
        """
        img_bgr = resize_max_dim(img_bgr, config.OCR_MAX_INPUT_DIM)
        reader = self._get_reader()
        results = reader.readtext(
            img_bgr,
            canvas_size=config.OCR_CANVAS_SIZE,
            batch_size=8,
            paragraph=False,
        )  # [(box, text, confidence), ...]

        detections = []
        boxes_for_draw = []
        lines = []

        for box, text, conf in results:
            xs = [float(p[0]) for p in box]
            ys = [float(p[1]) for p in box]
            x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)
            conf = float(conf)
            detections.append(
                {
                    "text": text,
                    "confidence": round(conf, 4),
                    "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                }
            )
            boxes_for_draw.append(
                {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "label": text, "confidence": conf}
            )
            lines.append(text)

        annotated = draw_boxes(img_bgr, boxes_for_draw)

        return {
            "full_text": "\n".join(lines).strip(),
            "detections": detections,
            "annotated_image": cv2_to_base64(annotated),
            "count": len(detections),
        }


def get_ocr_service() -> OCRService:
    return OCRService.instance()
