"""
main.py
--------
Entry point for the AI Vision Console backend.

Serves:
  - REST API under /api/*  (OCR, object detection, digit recognition, TTS)
  - The static frontend (frontend/) at "/"

Run with:
    python -m backend.main
or via the provided run.bat (Windows) / run.sh (Linux/Mac).
"""

from __future__ import annotations

import sys
import threading
import time
import webbrowser
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))  # allow `backend.*` imports

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import numpy as np

from backend import config
from backend.services.detection_service import get_detection_service
from backend.services.digit_service import get_digit_service
from backend.services.ocr_service import get_ocr_service
from backend.services.tts_service import synthesize_speech
from backend.utils.image_utils import bytes_to_cv2

app = FastAPI(
    title="AI Vision Console API",
    description="OCR + Object Recognition + Custom Digit Classifier + TTS",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _to_jsonable(obj):
    """
    Recursively convert numpy scalar/array types (which sneak in from
    OpenCV/PyTorch/EasyOCR/Ultralytics return values) into plain Python
    types. Defense-in-depth on top of the explicit float()/int() casts
    already done in each service -- prevents a repeat of the
    'Object of type int32/float32 is not JSON serializable' crash if a
    future model update returns numpy types from a new field.
    """
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def _read_upload(file: UploadFile) -> bytes:
    if file.content_type not in config.ALLOWED_IMAGE_TYPES:
        raise HTTPException(415, f"Unsupported file type: {file.content_type}")
    data = file.file.read()
    size_mb = len(data) / (1024 * 1024)
    if size_mb > config.MAX_UPLOAD_MB:
        raise HTTPException(413, f"File too large ({size_mb:.1f} MB > {config.MAX_UPLOAD_MB} MB)")
    return data


# ---------------------------------------------------------------- health --
@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "digit_model_trained": get_digit_service().is_trained,
        "ocr_ready": get_ocr_service().is_ready,
        "detection_ready": get_detection_service().is_ready,
    }


@app.on_event("startup")
def _warm_up_models():
    """
    Load OCR + detection models in a background thread as soon as the
    server starts, instead of on the first user request. This is what
    removes the "first click is really slow" experience -- by the time
    someone has opened the browser and clicked a tab, the models are
    usually already loaded.
    """
    if not config.WARM_UP_MODELS_ON_STARTUP:
        return

    def _load():
        print("[startup] Warming up OCR engine...")
        try:
            get_ocr_service().warm_up()
            print("[startup] OCR engine ready.")
        except Exception as exc:  # pragma: no cover
            print(f"[startup] OCR warm-up failed: {exc}")

        print("[startup] Warming up object detection model...")
        try:
            get_detection_service().warm_up()
            print("[startup] Object detection model ready.")
        except Exception as exc:  # pragma: no cover
            print(f"[startup] Detection warm-up failed: {exc}")

    threading.Thread(target=_load, daemon=True).start()


# ------------------------------------------------------------------- ocr --
@app.post("/api/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    try:
        img = bytes_to_cv2(_read_upload(file))
        result = get_ocr_service().recognize(img)
        return JSONResponse(_to_jsonable(result))
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(500, f"OCR failed: {exc}") from exc


# ----------------------------------------------------------- object det --
@app.post("/api/detect")
async def detect_endpoint(
    file: UploadFile = File(...),
    confidence: float = Form(None),
    quality: str = Form(None),
):
    try:
        img = bytes_to_cv2(_read_upload(file))
        result = get_detection_service().detect(img, confidence=confidence, quality=quality)
        return JSONResponse(_to_jsonable(result))
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(500, f"Object detection failed: {exc}") from exc


# --------------------------------------------------------------- digits --
@app.post("/api/digit")
async def digit_endpoint(file: UploadFile = File(...)):
    try:
        img = bytes_to_cv2(_read_upload(file))
        result = get_digit_service().predict(img)
        return JSONResponse(_to_jsonable(result))
    except FileNotFoundError as exc:
        raise HTTPException(409, str(exc)) from exc
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        raise HTTPException(500, f"Digit recognition failed: {exc}") from exc


# -------------------------------------------------------------------tts --
@app.post("/api/tts")
async def tts_endpoint(text: str = Form(...)):
    try:
        path = synthesize_speech(text)
        return FileResponse(path, media_type="audio/wav", filename="speech.wav")
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:  # pragma: no cover
        raise HTTPException(500, f"Speech synthesis failed: {exc}") from exc


# ------------------------------------------------------------- frontend --
app.mount("/", StaticFiles(directory=str(config.FRONTEND_DIR), html=True), name="frontend")


def _open_browser_when_ready():
    time.sleep(1.2)
    webbrowser.open(f"http://{config.HOST}:{config.PORT}")


def run():
    import uvicorn

    if config.AUTO_OPEN_BROWSER:
        threading.Thread(target=_open_browser_when_ready, daemon=True).start()

    print("=" * 60)
    print("  AI VISION CONSOLE — OCR + Object + Digit Recognition")
    print(f"  Serving at: http://{config.HOST}:{config.PORT}")
    print("=" * 60)

    uvicorn.run(app, host=config.HOST, port=config.PORT, log_level="info")


if __name__ == "__main__":
    run()
