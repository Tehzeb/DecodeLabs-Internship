"""
train.py  —  Run this to train the helmet detection model
Command : python train.py
"""
from ultralytics import YOLO
import torch, os

MODEL    = "yolov8n.pt"   # nano = smallest/fastest, downloads automatically
DATA     = "dataset.yaml"
EPOCHS   = 50
IMGSZ    = 640
BATCH    = 8              # lower to 4 if you get memory error
DEVICE   = "0" if torch.cuda.is_available() else "cpu"
PROJECT  = "runs"
NAME     = "helmet_v1"

print(f"\n{'='*52}")
print(f"  Helmet Detection — YOLOv8 Training")
print(f"  Device  : {'GPU' if DEVICE=='0' else 'CPU (slow but works)'}")
print(f"  Epochs  : {EPOCHS}")
print(f"{'='*52}\n")

model = YOLO(MODEL)
model.train(
    data     = DATA,
    epochs   = EPOCHS,
    imgsz    = IMGSZ,
    batch    = BATCH,
    project  = PROJECT,
    name     = NAME,
    device   = DEVICE,
    patience = 15,
    save     = True,
    plots    = True,
)
print(f"\n  Done!  Best weights → runs/{NAME}/weights/best.pt")
