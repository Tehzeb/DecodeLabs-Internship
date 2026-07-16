"""
train_digit_model.py
----------------------
Trains the custom DigitCNN on MNIST and saves weights to
backend/models/saved/digit_cnn.pth for the API to load at inference
time.

Run this once before starting the server (or the digit-recognition
tab will report the model as "not trained yet"):

    python -m backend.models.train_digit_model

Typical result on CPU: ~99% test accuracy in 5 epochs, ~2-4 minutes.
A training-curve plot is saved alongside the weights for the report.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

sys.path.append(str(Path(__file__).resolve().parents[2]))  # allow `backend.*` imports

from backend import config
from backend.models.digit_cnn import DigitCNN

EPOCHS = 5
BATCH_SIZE = 128
LEARNING_RATE = 1e-3
DATA_DIR = Path(__file__).resolve().parent / "data"


def get_dataloaders():
    transform = transforms.Compose(
        [
            transforms.RandomRotation(8),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ]
    )
    eval_transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))]
    )

    train_set = datasets.MNIST(DATA_DIR, train=True, download=True, transform=transform)
    test_set = datasets.MNIST(DATA_DIR, train=False, download=True, transform=eval_transform)

    train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_set, batch_size=256, shuffle=False, num_workers=0)
    return train_loader, test_loader


def evaluate(model, loader, device):
    model.eval()
    correct, total = 0, 0
    with torch.no_grad():
        for x, y in loader:
            x, y = x.to(device), y.to(device)
            preds = model(x).argmax(dim=1)
            correct += (preds == y).sum().item()
            total += y.size(0)
    return correct / total


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[train_digit_model] Using device: {device}")

    train_loader, test_loader = get_dataloaders()

    model = DigitCNN().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

    history = {"train_loss": [], "test_acc": []}

    for epoch in range(1, EPOCHS + 1):
        model.train()
        start = time.time()
        running_loss = 0.0

        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            loss = criterion(model(x), y)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * x.size(0)

        avg_loss = running_loss / len(train_loader.dataset)
        test_acc = evaluate(model, test_loader, device)
        history["train_loss"].append(avg_loss)
        history["test_acc"].append(test_acc)

        elapsed = time.time() - start
        print(
            f"Epoch {epoch}/{EPOCHS} | loss={avg_loss:.4f} | "
            f"test_acc={test_acc * 100:.2f}% | {elapsed:.1f}s"
        )

    config.SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), config.DIGIT_MODEL_PATH)
    print(f"[train_digit_model] Saved weights to {config.DIGIT_MODEL_PATH}")

    # Save a training curve for the project report / README
    fig, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(history["train_loss"], color="tab:red", marker="o", label="Train loss")
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Loss", color="tab:red")
    ax2 = ax1.twinx()
    ax2.plot(
        [a * 100 for a in history["test_acc"]],
        color="tab:blue", marker="s", label="Test accuracy (%)",
    )
    ax2.set_ylabel("Test accuracy (%)", color="tab:blue")
    plt.title("DigitCNN Training Curve")
    fig.tight_layout()
    curve_path = config.SAVED_MODELS_DIR / "training_curve.png"
    fig.savefig(curve_path, dpi=150)
    print(f"[train_digit_model] Saved training curve to {curve_path}")


if __name__ == "__main__":
    main()
