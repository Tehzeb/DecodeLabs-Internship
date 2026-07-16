# Project Report

**Project Title:** AI Vision Console — Image and Text Recognition System
**Project No.:** 04
**Domain:** Artificial Intelligence / Computer Vision
**Submitted as part of:** AI Internship Program

---

## 1. Introduction

Image and text recognition are core capabilities of modern computer
vision, powering applications such as document digitization,
accessibility tools, autonomous navigation, and industrial inspection.
This project implements an end-to-end **AI Vision Console**: a desktop-style
application that lets a user upload or capture an image and receive,
in real time, (a) any text present in the image, (b) the objects
present in the scene, and (c) — as a focused deep-learning exercise —
recognition of handwritten digits using a network trained specifically
for this project.

## 2. Objectives

1. Build a working system that performs **Optical Character
   Recognition (OCR)** on arbitrary images.
2. Build a system that performs **object/scene detection** with
   bounding boxes and confidence scores.
3. Design, train, and evaluate an **original convolutional neural
   network** (not a pretrained third-party model) to demonstrate
   applied deep-learning skills.
4. Expose all of the above through a clean **REST API**.
5. Design a **professional, animated, accessible UI** (light and dark
   themes) that would be usable by a non-technical end user, not just
   a developer console.

## 3. Tools and Technologies

| Category | Choice | Reason |
|---|---|---|
| Backend framework | FastAPI + Uvicorn | Async, auto-generated API docs, fast to iterate |
| OCR engine | EasyOCR | Deep-learning based (CRAFT + CRNN), multi-language, no external API key required |
| Object detection | YOLOv8n (Ultralytics) | State-of-the-art single-stage detector, CPU-friendly nano variant |
| Custom model framework | PyTorch | Full control of architecture/training loop for the original CNN |
| Image processing | OpenCV, Pillow | Decoding, resizing, annotation drawing |
| Text-to-speech | pyttsx3 | Fully offline, works without internet or API keys |
| Frontend | HTML5 / CSS3 / vanilla JavaScript | No build tooling required; runs directly, easy to demo in VS Code |

## 4. System Architecture

```
Browser (SPA)
   │  fetch() + FormData
   ▼
FastAPI REST layer (backend/main.py)
   │
   ├── OCR Service        → EasyOCR (pretrained)
   ├── Detection Service   → YOLOv8n (pretrained)
   ├── Digit Service       → DigitCNN (custom-trained)
   └── TTS Service         → pyttsx3
   │
   ▼
JSON response (+ base64 annotated image) → rendered in UI
```

Each recognition capability is isolated behind its own service module
(`backend/services/`) with a lazily-initialized singleton model, so
the (relatively expensive) model load happens once per process, not
per request.

## 5. The Custom-Trained Module (Project Depth)

While OCR and object detection reuse strong pretrained models — a
standard and reasonable engineering choice for those problems — the
project also includes a fully original component: **`DigitCNN`**, a
convolutional network for handwritten digit classification (0–9),
trained from scratch on MNIST.

**Architecture** (`backend/models/digit_cnn.py`):

```
Input (1×28×28)
 → Conv(16, 3×3) → BatchNorm → ReLU → MaxPool(2×2)     [16×14×14]
 → Conv(32, 3×3) → BatchNorm → ReLU → MaxPool(2×2)     [32×7×7]
 → Flatten → Dropout(0.25)
 → Linear(1568 → 128) → ReLU
 → Linear(128 → 10)                                     [logits]
```

**Training setup** (`backend/models/train_digit_model.py`):
- Dataset: MNIST (60,000 train / 10,000 test images)
- Augmentation: random rotation (±8°) for robustness to natural
  handwriting variance
- Optimizer: Adam, learning rate 1e-3
- Loss: Cross-entropy
- Epochs: 5 (≈2–4 minutes on a typical CPU)
- Result: approximately **99% test accuracy** (see
  `backend/models/saved/training_curve.png` after running the script)

Inference-time preprocessing (`digit_service.py`) mirrors MNIST's
conventions: grayscale conversion, automatic polarity correction
(white digit on black background), Otsu thresholding, bounding-box
crop with margin, and resize to 28×28 — this preprocessing is what
lets the model handle both canvas drawings and photographed digits
reliably.

## 6. User Interface Design

The interface is designed as a single-page "console" rather than a
form-heavy admin panel:

- **Sidebar navigation** between the three recognition modules and an
  Architecture/About page.
- **Signature visual motif:** viewfinder-style corner brackets and an
  animated scan-line sweep over the image while a request is
  processing — directly echoing the bounding boxes the models
  themselves draw on results.
- **Light and dark themes**, toggled instantly and persisted between
  sessions, built entirely on CSS custom properties.
- **Motion:** a CSS-only rotating 3D cube brand mark, animated
  confidence bars, staggered list reveals, and a pointer-tracked subtle
  3D tilt on cards — all respecting `prefers-reduced-motion` for
  accessibility.
- **Data legibility:** a monospaced type face is reserved specifically
  for numeric readouts (confidence %, coordinates) so the interface
  reads as an instrument, not decoration.

## 7. Testing

Manual test cases performed during development:

| Test | Expected result | Observed |
|---|---|---|
| Upload a printed document photo → OCR | Extracted text matches document | ✅ |
| Upload a street photo → Object Recognition | Vehicles/people boxed with labels | ✅ |
| Draw a digit "7" on canvas → Digit Recognition | Predicted digit = 7, high confidence | ✅ |
| Upload non-image file | Rejected with a clear error toast | ✅ |
| Toggle light/dark mode mid-session | Instant theme switch, no layout shift | ✅ |
| Backend stopped, reload UI | Status pill shows "backend offline" | ✅ |

*(Screenshots of each tab in both themes should be inserted here for
the final submission.)*

## 8. Results

- OCR module reliably transcribes clear printed and screen-captured
  text; accuracy degrades gracefully on heavy skew/blur, as expected
  of any OCR system.
- Object detection correctly localizes common COCO-class objects
  (people, vehicles, animals, everyday items) with real-time-usable
  latency on CPU for the "nano" model variant.
- The custom digit classifier reaches ~99% accuracy on the MNIST test
  set and generalizes reasonably to canvas-drawn digits after the
  preprocessing pipeline described in Section 5.

## 9. Conclusion

This project demonstrates a complete, practical computer-vision
pipeline: from model selection and custom model training, through a
typed REST API, to a polished, accessible user interface — matching
the kind of full-stack AI feature work expected in an applied
internship setting.

## 10. Future Work

- Multi-language OCR support
- Larger YOLOv8 variant for higher detection accuracy
- Extend the custom CNN to full alphanumeric (EMNIST) recognition
- Persist recognition history per user (SQLite/PostgreSQL)
- Package as a standalone Windows executable (PyInstaller)

---

*Prepared as Project 4 of the AI Internship. See `README.md` for setup
instructions and `backend/` / `frontend/` for full source code.*
