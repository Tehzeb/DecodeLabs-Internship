"""
config.py
---------
Central configuration for the AI Vision Console backend.
Keeping all tunables in one place makes the project easy to defend
in a viva/demo: "where is X configured?" -> config.py.
"""

import os
from pathlib import Path

# --- Paths -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
SAVED_MODELS_DIR = BASE_DIR / "models" / "saved"
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(exist_ok=True)
SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)

DIGIT_MODEL_PATH = SAVED_MODELS_DIR / "digit_cnn.pth"

# --- Server --------------------------------------------------------------
HOST = os.environ.get("APP_HOST", "127.0.0.1")
PORT = int(os.environ.get("APP_PORT", 8000))
AUTO_OPEN_BROWSER = True

# --- OCR -------------------------------------------------------------
OCR_LANGUAGES = ["en"]          # add e.g. "ur" for Urdu, "ar" for Arabic if needed
OCR_GPU = False                  # set True if a CUDA GPU + torch-cuda is available
# EasyOCR's internal detector upscales to this size before running —
# the default (2560) is the single biggest cause of slow CPU inference.
# 1280 is a good speed/accuracy balance for typical photos/screenshots.
OCR_CANVAS_SIZE = 1280
OCR_MAX_INPUT_DIM = 1100         # image is downscaled to this before OCR even runs
WARM_UP_MODELS_ON_STARTUP = True  # load models in the background at server start,
                                   # not on the first user request

# --- Object Detection --------------------------------------------------
# Three quality tiers the user can pick in the UI. "Balanced" is the
# default. Larger models are meaningfully more accurate on cluttered,
# close-up, or unusually-angled real-world photos (exactly the kind of
# product photography that trips up the nano model), at the cost of
# slower inference and a larger one-time weights download.
DETECTION_QUALITY_PRESETS = {
    "fast": {"weights": "yolov8n.pt", "imgsz": 640, "augment": False},
    "balanced": {"weights": "yolov8s.pt", "imgsz": 768, "augment": False},
    "accurate": {"weights": "yolov8m.pt", "imgsz": 960, "augment": True},
}
DEFAULT_DETECTION_QUALITY = "balanced"
YOLO_CONFIDENCE_THRESHOLD = 0.25   # COCO-standard default; 0.35 was dropping valid objects
YOLO_IOU_THRESHOLD = 0.45          # NMS overlap threshold
YOLO_AGNOSTIC_NMS = True           # suppresses overlapping boxes of *different* classes
                                    # on the same object, which was the main cause of
                                    # "two boxes / wrong label" on a single object

# NOTE ON MODEL VOCABULARY: these models are trained on the COCO dataset,
# which has a fixed list of 80 everyday object classes. COCO does NOT
# include a "watch"/"wristwatch" class -- the closest is "clock" -- so a
# wristwatch will sometimes be labeled "clock" or something else entirely
# by any COCO-trained detector, regardless of model size. This is a
# vocabulary limitation of the dataset, not a bug. See README section
# "Performance & accuracy notes" for the full COCO class list and options
# (e.g. fine-tuning on custom classes) if you need "watch" specifically.

# --- Digit Recognition (custom-trained module) --------------------------
DIGIT_IMG_SIZE = 28
DIGIT_CLASSES = list(range(10))

# --- Text to Speech ------------------------------------------------------
TTS_RATE = 175
TTS_VOLUME = 1.0

# --- Misc -----------------------------------------------------------
MAX_UPLOAD_MB = 15
ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/bmp"}
