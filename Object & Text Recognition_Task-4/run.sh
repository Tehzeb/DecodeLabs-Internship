#!/usr/bin/env bash
# ============================================================
#  AI Vision Console — Linux/Mac launcher
# ============================================================
set -e

if [ ! -d ".venv" ]; then
    echo "[setup] Creating virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "[setup] Installing dependencies (first run only)..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt

if [ ! -f "backend/models/saved/digit_cnn.pth" ]; then
    echo "[setup] Custom digit model not found. Training it now (~2-4 min on CPU)..."
    python -m backend.models.train_digit_model
fi

echo "[run] Starting AI Vision Console..."
python -m backend.main
