"""
webcam_demo.py  —  Live Helmet Detection via Webcam
====================================================
Run this AFTER training is complete.

Command:
    python webcam_demo.py

Controls while running:
    Q  —  quit
    S  —  save a screenshot to output/screenshots/
    R  —  reset violation counter to zero
    P  —  pause / resume

What you will see:
    Green box  +  "Helmet  94%"   —  person wearing helmet  ✓
    Red box    +  "No Helmet 87%" —  person NOT wearing helmet  ✗

How to demonstrate to your professor:
    1. Run this file
    2. Wear your helmet in front of webcam  →  green box appears
    3. Remove helmet                        →  box turns red instantly
    4. Press S to take a screenshot         →  saved to output/screenshots/
"""

import cv2
import os
import time
import datetime
import numpy as np
from ultralytics import YOLO

# ── Configuration ─────────────────────────────────────────────────────────────
WEIGHTS = "runs/detect/runs/helmet_v1/weights/best.pt"  # trained model
CONF        = 0.45       # confidence threshold (lower = detects more, may add noise)
WEBCAM_ID   = 0          # 0 = built-in webcam, 1 = external USB webcam
WINDOW_NAME = "Helmet Detection  |  Q=quit  S=screenshot  R=reset  P=pause"

# Colors  BGR format
GREEN       = (30,  180,  80)    # helmet ✓
RED         = (210,  40,  40)    # no helmet ✗
WHITE       = (255, 255, 255)
BLACK       = (10,   10,  10)
YELLOW      = (0,   200, 220)
PANEL_BG    = (25,   25,  25)

# Class info
CLASS_COLOR = {0: GREEN,  1: RED}
CLASS_LABEL = {0: "Helmet", 1: "No Helmet"}
CLASS_ICON  = {0: "✓", 1: "✗"}
# ──────────────────────────────────────────────────────────────────────────────


def load_model():
    """Load trained weights. Gives clear error if training not done yet."""
    if not os.path.exists(WEIGHTS):
        print("\n" + "="*55)
        print("  ERROR: Trained weights not found!")
        print(f"  Expected file: {WEIGHTS}")
        print("")
        print("  You must run training first:")
        print("      python train.py")
        print("")
        print("  Training takes 2-8 hours on CPU.")
        print("="*55 + "\n")
        raise SystemExit(1)
    print(f"\n  Loading model from {WEIGHTS} ...")
    model = YOLO(WEIGHTS)
    print("  Model loaded successfully!\n")
    return model


def draw_box(frame, x1, y1, x2, y2, label, conf, color):
    """Draw one detection box with label and confidence."""
    # Main rectangle — 2px border
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Corner accents (make it look professional)
    corner = 14
    thick  = 3
    # Top-left
    cv2.line(frame, (x1, y1), (x1+corner, y1), color, thick)
    cv2.line(frame, (x1, y1), (x1, y1+corner), color, thick)
    # Top-right
    cv2.line(frame, (x2, y1), (x2-corner, y1), color, thick)
    cv2.line(frame, (x2, y1), (x2, y1+corner), color, thick)
    # Bottom-left
    cv2.line(frame, (x1, y2), (x1+corner, y2), color, thick)
    cv2.line(frame, (x1, y2), (x1, y2-corner), color, thick)
    # Bottom-right
    cv2.line(frame, (x2, y2), (x2-corner, y2), color, thick)
    cv2.line(frame, (x2, y2), (x2, y2-corner), color, thick)

    # Label background + text
    text = f"{label}  {conf:.0%}"
    (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
    # Place label above box, or below if too close to top
    lx = x1
    ly = y1 - 10 if y1 - 10 > th + 4 else y2 + th + 10
    cv2.rectangle(frame, (lx, ly-th-6), (lx+tw+10, ly+2), color, -1)
    cv2.putText(frame, text, (lx+5, ly-2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, WHITE, 2)


def draw_panel(frame, helmet_count, violation_count, total_violations,
               fps, paused):
    """Draw the info panel on the left side of the frame."""
    h, w = frame.shape[:2]
    panel_w = 210

    # Semi-transparent dark panel
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (panel_w, h), PANEL_BG, -1)
    cv2.addWeighted(overlay, 0.75, frame, 0.25, 0, frame)

    # Title
    cv2.putText(frame, "HELMET DETECTION", (8, 24),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, WHITE, 1)
    cv2.line(frame, (8, 32), (panel_w-8, 32), (80,80,80), 1)

    # LIVE / PAUSED badge
    if paused:
        cv2.rectangle(frame, (8, 40), (80, 62), YELLOW, -1)
        cv2.putText(frame, " PAUSED", (10, 57),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, BLACK, 1)
    else:
        cv2.rectangle(frame, (8, 40), (65, 62), (0,0,180), -1)
        cv2.circle(frame, (20, 51), 6, RED, -1)
        cv2.putText(frame, " LIVE", (28, 57),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, WHITE, 1)

    # FPS
    cv2.putText(frame, f"FPS: {fps:.1f}", (120, 57),
                cv2.FONT_HERSHEY_SIMPLEX, 0.48, (180,180,180), 1)

    # Current frame counts
    cv2.line(frame, (8, 70), (panel_w-8, 70), (60,60,60), 1)
    cv2.putText(frame, "THIS FRAME", (8, 88),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (150,150,150), 1)

    # Helmet count (green)
    cv2.rectangle(frame, (8, 95), (panel_w-8, 120), (15,50,20), -1)
    cv2.putText(frame, f"  Helmet:    {helmet_count}", (10, 113),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, GREEN, 1)

    # Violation count (red)
    cv2.rectangle(frame, (8, 124), (panel_w-8, 149), (50,15,15), -1)
    cv2.putText(frame, f"  No Helmet: {violation_count}", (10, 143),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, RED, 1)

    # Total violations
    cv2.line(frame, (8, 158), (panel_w-8, 158), (60,60,60), 1)
    cv2.putText(frame, "TOTAL VIOLATIONS", (8, 176),
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (150,150,150), 1)
    vcolor = RED if total_violations > 0 else GREEN
    cv2.putText(frame, f"  {total_violations}", (10, 208),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, vcolor, 2)

    # Status message at bottom of panel
    cv2.line(frame, (8, h-80), (panel_w-8, h-80), (60,60,60), 1)
    status_lines = ["Q - Quit", "S - Screenshot", "R - Reset count", "P - Pause"]
    for i, line in enumerate(status_lines):
        cv2.putText(frame, line, (10, h-60+i*16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, (130,130,130), 1)


def draw_alert_banner(frame, violation_count):
    """Show red VIOLATION banner at top if someone has no helmet."""
    if violation_count == 0:
        return
    h, w = frame.shape[:2]
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, 38), (180, 0, 0), -1)
    cv2.addWeighted(overlay, 0.85, frame, 0.15, 0, frame)
    msg = f"  ✗  HELMET VIOLATION DETECTED  —  {violation_count} person(s) without helmet  ✗"
    cv2.putText(frame, msg, (8, 26),
                cv2.FONT_HERSHEY_SIMPLEX, 0.62, WHITE, 2)


def save_screenshot(frame, count):
    """Save current frame as a screenshot."""
    folder = os.path.join("output", "screenshots")
    os.makedirs(folder, exist_ok=True)
    ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(folder, f"screenshot_{ts}.jpg")
    cv2.imwrite(path, frame)
    print(f"  Screenshot saved → {path}")
    return path


def run_webcam(model):
    """Main webcam loop."""
    cap = cv2.VideoCapture(WEBCAM_ID)

    if not cap.isOpened():
        print("\n  ERROR: Cannot open webcam.")
        print("  Make sure your webcam is connected and not used by another app.")
        print("  Try changing WEBCAM_ID from 0 to 1 at the top of this file.\n")
        return

    # Try to set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    actual_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"  Webcam opened  —  {actual_w}×{actual_h}")
    print(f"  Press Q to quit  |  S to screenshot  |  R to reset  |  P to pause")
    print(f"\n  Tip for demo: wear helmet → green box appears")
    print(f"                remove helmet → red box + VIOLATION banner\n")

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(WINDOW_NAME, actual_w + 210, actual_h)

    total_violations = 0
    screenshot_count = 0
    paused           = False
    paused_frame     = None

    # FPS tracking
    fps        = 0.0
    fps_buffer = []
    prev_time  = time.time()

    while True:
        # ── Key handling ──────────────────────────────────────────────────────
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") or key == 27:      # Q or Escape
            break
        elif key == ord("s"):                  # screenshot
            if paused and paused_frame is not None:
                save_screenshot(paused_frame, screenshot_count)
            else:
                pass   # will save after drawing
            screenshot_count += 1
        elif key == ord("r"):                  # reset counter
            total_violations = 0
            print("  Violation counter reset to 0")
        elif key == ord("p"):                  # pause
            paused = not paused
            print("  Paused" if paused else "  Resumed")

        # ── Pause logic ───────────────────────────────────────────────────────
        if paused and paused_frame is not None:
            cv2.imshow(WINDOW_NAME, paused_frame)
            continue

        # ── Capture frame ─────────────────────────────────────────────────────
        ret, frame = cap.read()
        if not ret:
            print("  Webcam read failed. Reconnect webcam and restart.")
            break

        # Flip horizontally (mirror effect — more natural for live demo)
        frame = cv2.flip(frame, 1)

        # ── Run YOLOv8 detection ──────────────────────────────────────────────
        results = model.predict(frame, conf=CONF, verbose=False)[0]

        helmet_count    = 0
        violation_count = 0

        for box in results.boxes:
            cls  = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Shift boxes right to avoid overlap with side panel
            x1 += 210; x2 += 210

            color = CLASS_COLOR.get(cls, WHITE)
            label = CLASS_LABEL.get(cls, "?")

            draw_box(frame, x1, y1, x2, y2, label, conf, color)

            if cls == 0:
                helmet_count    += 1
            else:
                violation_count += 1
                total_violations += 1

        # ── FPS calculation ───────────────────────────────────────────────────
        now       = time.time()
        fps_inst  = 1.0 / max(now - prev_time, 1e-6)
        fps_buffer.append(fps_inst)
        if len(fps_buffer) > 15:
            fps_buffer.pop(0)
        fps       = sum(fps_buffer) / len(fps_buffer)
        prev_time = now

        # ── Draw UI ───────────────────────────────────────────────────────────
        draw_panel(frame, helmet_count, violation_count,
                   total_violations, fps, paused)
        draw_alert_banner(frame, violation_count)

        # ── Handle screenshot key (save after drawing) ─────────────────────
        if key == ord("s"):
            save_screenshot(frame, screenshot_count)

        paused_frame = frame.copy()
        cv2.imshow(WINDOW_NAME, frame)

    cap.release()
    cv2.destroyAllWindows()
    print(f"\n  Demo ended.")
    print(f"  Total violations recorded this session: {total_violations}")
    print(f"  Screenshots saved to: output/screenshots/")


if __name__ == "__main__":
    print("\n" + "="*55)
    print("  HELMET DETECTION — LIVE WEBCAM DEMO")
    print("="*55)
    model = load_model()
    run_webcam(model)