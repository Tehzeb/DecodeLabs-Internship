# AI Vision Console
### Image & Text Recognition — Internship Project 04

A hybrid computer-vision system with a professional, animated desktop-style
web console (light + dark mode). It combines **three recognition modules**
behind a single FastAPI backend:

| Module | Model | Type |
|---|---|---|
| Text Recognition (OCR) | EasyOCR (CRAFT detector + CRNN recognizer) | Pretrained |
| Object / Scene Recognition | YOLOv8n (Ultralytics, COCO-trained) | Pretrained |
| Handwritten Digit Recognition | Custom CNN (`DigitCNN`) | **Trained from scratch in this repo, on MNIST** |
| Read-aloud | pyttsx3 (offline, SAPI5 on Windows) | Utility |

The third module is what gives this project real depth: it isn't just
wiring up existing APIs — it includes the network architecture, the
training script, and the saved weights, so it can be explained and
defended like any original piece of ML work.

---

## 1. Requirements

- **Windows 11** (also works on Linux/Mac)
- **Python 3.10 or 3.11** — https://www.python.org/downloads/ (check "Add
  Python to PATH" during install)
- **VS Code** with the *Python* extension
- Internet connection for first run (downloads model weights)
- ~3 GB free disk space (PyTorch + model weights)

---

## 2. Project structure

```
AI_Vision_Console/
├── backend/
│   ├── main.py                    # FastAPI app + all API routes
│   ├── config.py                  # all tunables in one place
│   ├── services/
│   │   ├── ocr_service.py         # EasyOCR wrapper
│   │   ├── detection_service.py   # YOLOv8 wrapper
│   │   ├── digit_service.py       # custom CNN inference
│   │   └── tts_service.py         # pyttsx3 wrapper
│   ├── models/
│   │   ├── digit_cnn.py           # custom CNN architecture
│   │   ├── train_digit_model.py   # training script (run this once)
│   │   └── saved/                 # trained weights land here
│   └── utils/image_utils.py       # decode/encode/annotate helpers
├── frontend/
│   ├── index.html
│   ├── css/style.css              # design system, animations, themes
│   └── js/app.js                  # SPA logic, API calls, canvas drawing
├── requirements.txt
├── run.bat                        # one-click Windows launcher
├── run.sh                         # Linux/Mac launcher
└── README.md
```

---

## 3. Setup in VS Code (Windows 11)

1. **Open the project folder**
   `File → Open Folder…` → select `AI_Vision_Console`.

2. **Open a terminal in VS Code**
   `` Ctrl + ` `` (backtick), make sure it's a "Command Prompt" or
   "PowerShell" terminal.

3. **Easiest option — just run the launcher:**
   ```bat
   run.bat
   ```
   This creates a virtual environment, installs everything, trains the
   digit model on first run, and opens your browser automatically.

4. **Manual option (equivalent, if you like to see every step):**
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python -m backend.models.train_digit_model
   python -m backend.main
   ```

5. Your browser opens automatically at **http://127.0.0.1:8000**. If it
   doesn't, open it manually.

> **VS Code tip:** select the `.venv` interpreter via
> `Ctrl+Shift+P → Python: Select Interpreter` so linting/autocomplete and
> "Run ▶" both use the right environment.

---

## 4. Using the app

- **Text Recognition tab** — drag & drop or click to upload an image with
  text. Click *Run Text Recognition*. Extracted text appears with a copy
  button and a 🔊 *Read aloud* button (server-side TTS).
- **Object Recognition tab** — upload any photo; detected objects are
  drawn as labeled boxes on the image, plus a ranked confidence list.
- **Digit Recognition tab** — draw a digit (0–9) on the black pad with
  your mouse/touch, or upload a digit image, then click *Recognize
  Digit*. A live bar chart shows the model's confidence across all 10
  classes.
- **Architecture & About tab** — a one-page summary of the system for
  demos/vivas.

Toggle **light/dark mode** from the sun/moon switch in the top bar — the
whole interface (including chart colors) transitions smoothly.

---

## 5. Retraining the digit model

The CNN is fully custom and takes only a couple of minutes to retrain on
CPU:

```bat
python -m backend.models.train_digit_model
```

This downloads MNIST (first run only), trains for 5 epochs, prints
per-epoch loss/accuracy, saves `backend/models/saved/digit_cnn.pth`, and
writes a `training_curve.png` you can drop straight into your project
report.

To experiment (more epochs, deeper network, data augmentation), edit
`backend/models/digit_cnn.py` and `train_digit_model.py` — both are
short and heavily commented.

---

## 6. API reference (for your report / demo)

| Method | Endpoint | Body | Returns |
|---|---|---|---|
| GET | `/api/health` | – | backend + model status |
| POST | `/api/ocr` | `file` (image) | text regions, full text, annotated image |
| POST | `/api/detect` | `file` (image) | detected objects, tally, annotated image |
| POST | `/api/digit` | `file` (image) | predicted digit + full probability vector |
| POST | `/api/tts` | `text` (form field) | WAV audio stream |

All endpoints are also visible interactively at
**http://127.0.0.1:8000/docs** (FastAPI's auto-generated Swagger UI) —
useful for demonstrating the API directly to your supervisor.

---

## 7. Design notes

- **Signature visual motif:** viewfinder-style corner brackets + an
  animated scan-line sweep on the image preview while a request is in
  flight — a direct visual echo of what the models themselves draw
  (bounding boxes) on the result.
- **3D:** a CSS-only rotating cube mark in the sidebar (`prefers-reduced-motion`
  aware) plus a subtle pointer-tracked 3D tilt on the main cards.
- **Typography:** Space Grotesk (display) + Inter (body) + JetBrains Mono
  (data/readouts) — the mono face is reserved for numbers/labels to keep
  the "console" feel functional rather than decorative.
- Full light/dark theming via CSS custom properties, persisted in
  `localStorage`.

---

## 8. Performance & accuracy notes (read this if results look off)

- **Models now warm up at server startup** instead of on the first
  click — you'll see `[startup] OCR engine ready.` / `[startup] Object
  detection model ready.` in the terminal a few seconds after launch.
- **OCR crash fixed:** EasyOCR returns box coordinates and confidence
  scores as NumPy `int32`/`float32` values, which Python's default JSON
  encoder cannot serialize — this was the exact cause of the "Object of
  type int32 is not JSON serializable" error. All numeric values from
  every model (OCR, detection, digit) are now explicitly cast to native
  Python types before being returned, plus a global safety net
  (`_to_jsonable` in `backend/main.py`) catches anything that slips
  through in the future.
- **OCR speed:** EasyOCR is genuinely CPU-heavy; `OCR_CANVAS_SIZE` in
  `config.py` (1280 vs. EasyOCR's own default of 2560) is the main speed
  lever — lower it further if needed. An NVIDIA GPU + `OCR_GPU = True`
  gives a large speedup.
- **Object detection now has three quality tiers**, selectable in the UI
  (Object Recognition tab):

  | Tier | Model | Resolution | Notes |
  |---|---|---|---|
  | Fast | yolov8n | 640px | quickest, least accurate |
  | Balanced (default) | yolov8s | 768px | good general tradeoff |
  | Accurate | yolov8m + test-time augmentation | 960px | best for cluttered/close-up photos, slower, larger download |

  Try **Accurate** specifically for close-up product-style photos
  (phone/laptop/watch on a patterned background, etc.) — this is exactly
  the scenario where the smaller models struggle most.

- **"Wrong label" on overlapping boxes:** every object class now gets
  its own consistent color instead of one flat color for every box, so
  overlapping/adjacent detections are visually unambiguous.

- **Important: the detector's vocabulary is fixed at 80 COCO classes.**
  No amount of tuning, confidence adjustment, or model upgrade will make
  it output a word that isn't in this list — most notably, **there is no
  "watch" class**. A wristwatch will be labeled with whatever COCO class
  the model finds visually closest (commonly "clock", occasionally
  something less intuitive like "scissors" due to the strap shape). This
  is a dataset limitation, not a bug. The full class list:

  ```
  person, bicycle, car, motorcycle, airplane, bus, train, truck, boat,
  traffic light, fire hydrant, stop sign, parking meter, bench, bird,
  cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe, backpack,
  umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports
  ball, kite, baseball bat, baseball glove, skateboard, surfboard,
  tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl,
  banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza,
  donut, cake, chair, couch, potted plant, bed, dining table, toilet,
  tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven,
  toaster, sink, refrigerator, book, clock, vase, scissors, teddy bear,
  hair drier, toothbrush
  ```

  If exact "watch" (or any other non-COCO label) recognition is a hard
  requirement for your demo, the real fix is training/fine-tuning a
  detector on a custom-labeled dataset that includes that class — see
  "Possible extensions" below. This is genuinely a different, larger
  project than what pretrained COCO models can offer out of the box, so
  it's listed as future work rather than bundled here.

- **Non-canonical angles/close-ups are harder for any pretrained
  detector**, including humans-in-a-hurry — COCO's training photos are
  mostly natural, medium-distance scene shots, not top-down product
  photography on textured backgrounds. "Accurate" mode plus good, even
  lighting and a less extreme angle will generally improve results
  noticeably.

## 9. Troubleshooting

- **"Digit model isn't trained yet"** → run
  `python -m backend.models.train_digit_model` and restart the server.
- **First OCR/detection request is slow** → EasyOCR and YOLO weights
  initialize lazily on first use; subsequent requests are fast.
- **`pyttsx3` produces no audio on Windows** → ensure at least one voice
  is installed under *Settings → Time & Language → Speech*.
- **Port already in use** → change `APP_PORT` in `backend/config.py`.

---

## 10. Possible extensions (for a "future work" slide)

- Multi-language OCR (EasyOCR supports 80+ languages — add to
  `OCR_LANGUAGES` in `config.py`)
- Swap YOLOv8n for YOLOv8m/l for higher accuracy (slower)
- Fine-tune the digit CNN on EMNIST for full alphanumeric recognition
- Add user accounts + history using a small SQLite database
- Package as a native `.exe` with PyInstaller for zero-setup distribution
