"""
image_utils.py
---------------
Shared helpers for decoding uploaded images, encoding results back to
base64 for the frontend, and drawing annotation overlays (bounding
boxes / labels) in a single consistent visual style.
"""

from __future__ import annotations

import base64
import io
from typing import Iterable

import cv2
import numpy as np
from PIL import Image

# BGR colors (OpenCV) used for annotation overlays
COLOR_PRIMARY = (255, 209, 0)     # electric cyan-ish accent in BGR -> tuned below
COLOR_BOX = (0, 200, 255)         # amber/cyan mix, readable on light+dark photos
COLOR_TEXT_BG = (20, 20, 20)


def bytes_to_cv2(image_bytes: bytes) -> np.ndarray:
    """Decode raw uploaded bytes into an OpenCV BGR image."""
    pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(pil_img)
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)


def cv2_to_base64(img_bgr: np.ndarray, fmt: str = ".png") -> str:
    """Encode an OpenCV BGR image to a base64 data-URI string."""
    success, buffer = cv2.imencode(fmt, img_bgr)
    if not success:
        raise ValueError("Failed to encode image")
    b64 = base64.b64encode(buffer).decode("utf-8")
    mime = "image/png" if fmt == ".png" else "image/jpeg"
    return f"data:{mime};base64,{b64}"


def _color_for_label(label: str) -> tuple:
    """
    Deterministically map a class label to a distinct, readable color.
    Using one color per class (instead of one flat color for every box)
    is what makes labels unambiguous when boxes overlap or a scene is
    cluttered with several detections.
    """
    h = (hash(label) % 180 + 180) % 180  # OpenCV HSV hue range is 0-179
    hsv = np.uint8([[[h, 200, 255]]])  # high saturation/value = vivid, readable
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)[0][0]
    return int(bgr[0]), int(bgr[1]), int(bgr[2])


def draw_boxes(
    img_bgr: np.ndarray,
    boxes: Iterable[dict],
    text_color=(12, 12, 12),
) -> np.ndarray:
    """
    Draw labeled bounding boxes on a copy of img_bgr, one distinct
    color per class label so overlapping/adjacent detections stay
    visually unambiguous.
    Each box dict must have: x1, y1, x2, y2, label, confidence
    """
    out = img_bgr.copy()
    img_h, img_w = out.shape[:2]

    # draw boxes first (thin), then all labels on top (so text is never
    # occluded by a neighboring box's edge)
    boxes = list(boxes)
    for b in boxes:
        x1, y1, x2, y2 = int(b["x1"]), int(b["y1"]), int(b["x2"]), int(b["y2"])
        color = _color_for_label(str(b["label"]))
        cv2.rectangle(out, (x1, y1), (x2, y2), color, 2, lineType=cv2.LINE_AA)

    for b in boxes:
        x1, y1, x2, y2 = int(b["x1"]), int(b["y1"]), int(b["x2"]), int(b["y2"])
        color = _color_for_label(str(b["label"]))
        label = f'{b["label"]} {b["confidence"] * 100:.0f}%'

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale, thickness = 0.5, 1
        (tw, th), baseline = cv2.getTextSize(label, font, scale, thickness)

        # place label just above the box; if that would go off-image,
        # place it just inside the top edge instead
        if y1 - th - 10 >= 0:
            bg_top, bg_bottom = y1 - th - 10, y1
            text_y = y1 - 6
        else:
            bg_top, bg_bottom = y1, y1 + th + 10
            text_y = y1 + th + 4

        bg_left = max(0, min(x1, img_w - tw - 8))
        cv2.rectangle(out, (bg_left, bg_top), (bg_left + tw + 8, bg_bottom), color, -1)
        cv2.putText(
            out, label, (bg_left + 4, text_y),
            font, scale, text_color, thickness, cv2.LINE_AA,
        )
    return out


def resize_max_dim(img_bgr: np.ndarray, max_dim: int = 1280) -> np.ndarray:
    """Downscale large images before inference to keep latency low."""
    h, w = img_bgr.shape[:2]
    scale = max_dim / max(h, w)
    if scale >= 1:
        return img_bgr
    return cv2.resize(img_bgr, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
