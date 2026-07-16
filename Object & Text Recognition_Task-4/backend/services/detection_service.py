"""
detection_service.py
----------------------
Object / scene recognition powered by pretrained YOLOv8 models
(Ultralytics), trained on the COCO dataset (80 everyday object classes).

Three quality tiers are available (see config.DETECTION_QUALITY_PRESETS):
  - fast:      yolov8n, imgsz 640  -- quickest, least accurate
  - balanced:  yolov8s, imgsz 768  -- default
  - accurate:  yolov8m, imgsz 960 + test-time augmentation -- slowest,
               most accurate; recommended for cluttered or close-up
               product-style photos where the smaller tiers struggle

Each tier's weights file is downloaded automatically by the ultralytics
library the first time that tier is used (requires internet once per
tier). Only the default tier is warmed up at startup so first boot
doesn't have to download all three.

IMPORTANT LIMITATION: COCO's 80 classes do not include "watch" -- the
closest available class is "clock". No amount of tuning will make a
COCO-trained model output "watch", because that word isn't in its
vocabulary. See README for the full class list and options if exact
"watch" labeling matters for your demo.
"""

from __future__ import annotations

import threading
from typing import Optional

from ultralytics import YOLO

from backend import config
from backend.utils.image_utils import draw_boxes, cv2_to_base64, resize_max_dim


class DetectionService:
    _instance: Optional["DetectionService"] = None
    _lock = threading.Lock()

    def __init__(self):
        self._models: dict[str, YOLO] = {}
        self._model_lock = threading.Lock()

    @classmethod
    def instance(cls) -> "DetectionService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = DetectionService()
        return cls._instance

    def _resolve_quality(self, quality: str | None) -> str:
        if quality and quality in config.DETECTION_QUALITY_PRESETS:
            return quality
        return config.DEFAULT_DETECTION_QUALITY

    def _get_model(self, quality: str) -> YOLO:
        if quality not in self._models:
            with self._model_lock:
                if quality not in self._models:
                    weights = config.DETECTION_QUALITY_PRESETS[quality]["weights"]
                    self._models[quality] = YOLO(weights)
        return self._models[quality]

    def warm_up(self) -> None:
        """Load the default-tier model ahead of the first request (called at server startup)."""
        self._get_model(config.DEFAULT_DETECTION_QUALITY)

    @property
    def is_ready(self) -> bool:
        return config.DEFAULT_DETECTION_QUALITY in self._models

    def detect(
        self,
        img_bgr,
        confidence: float | None = None,
        quality: str | None = None,
    ) -> dict:
        quality = self._resolve_quality(quality)
        preset = config.DETECTION_QUALITY_PRESETS[quality]

        img_bgr = resize_max_dim(img_bgr, 1600)
        model = self._get_model(quality)
        results = model.predict(
            img_bgr,
            conf=confidence if confidence is not None else config.YOLO_CONFIDENCE_THRESHOLD,
            iou=config.YOLO_IOU_THRESHOLD,
            agnostic_nms=config.YOLO_AGNOSTIC_NMS,
            imgsz=preset["imgsz"],
            augment=preset["augment"],
            verbose=False,
        )[0]

        detections = []
        boxes_for_draw = []
        tally: dict[str, int] = {}

        names = results.names
        for box in results.boxes:
            cls_id = int(box.cls[0])
            label = names.get(cls_id, str(cls_id)) if isinstance(names, dict) else names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = [float(v) for v in box.xyxy[0].tolist()]

            detections.append(
                {
                    "label": label,
                    "confidence": round(conf, 4),
                    "box": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                }
            )
            boxes_for_draw.append(
                {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "label": label, "confidence": conf}
            )
            tally[label] = tally.get(label, 0) + 1

        annotated = draw_boxes(img_bgr, boxes_for_draw)

        return {
            "detections": detections,
            "tally": tally,
            "annotated_image": cv2_to_base64(annotated),
            "count": len(detections),
            "quality_used": quality,
        }


def get_detection_service() -> DetectionService:
    return DetectionService.instance()
