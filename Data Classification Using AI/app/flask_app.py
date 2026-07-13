"""
flask_app.py
--------------
Deployment-ready REST API exposing the best trained model.

Run with (from the project root, after main.py has been run once):
    python app/flask_app.py

Endpoints
---------
GET  /                 -> health check / API info
GET  /health            -> {"status": "ok"}
GET  /model-info         -> metadata about the deployed model
POST /predict            -> classify a single sample (JSON body)
POST /predict-batch       -> classify multiple samples (JSON list)

Example request (PowerShell / curl):

curl -X POST http://127.0.0.1:5000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"alcohol\": 13.2, \"malic_acid\": 1.78, \"ash\": 2.14, \"alcalinity_of_ash\": 11.2, \"magnesium\": 100, \"total_phenols\": 2.65, \"flavanoids\": 2.76, \"nonflavanoid_phenols\": 0.26, \"proanthocyanins\": 1.28, \"color_intensity\": 4.38, \"hue\": 1.05, \"od280/od315_of_diluted_wines\": 3.4, \"proline\": 1050}"
"""

from pathlib import Path
import json

import joblib
import pandas as pd
from flask import Flask, jsonify, request

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

app = Flask(__name__)

# ---- Load artifacts once at startup ----
scaler = joblib.load(MODELS_DIR / "scaler.pkl")
feature_cols = joblib.load(MODELS_DIR / "feature_columns.pkl")
best_model = joblib.load(MODELS_DIR / "best_model.pkl")
with open(MODELS_DIR / "best_model_name.json") as f:
    best_model_name = json.load(f)["best_model"]

CLASS_LABELS = {0: "class_0", 1: "class_1", 2: "class_2"}


def make_prediction(record: dict):
    missing = [c for c in feature_cols if c not in record]
    if missing:
        raise ValueError(f"Missing required features: {missing}")

    X = pd.DataFrame([record])[feature_cols]
    X_scaled = pd.DataFrame(scaler.transform(X), columns=feature_cols)
    pred = int(best_model.predict(X_scaled)[0])

    result = {"predicted_class": pred, "predicted_label": CLASS_LABELS[pred]}
    if hasattr(best_model, "predict_proba"):
        proba = best_model.predict_proba(X_scaled)[0]
        result["probabilities"] = {CLASS_LABELS[i]: round(float(p), 4) for i, p in enumerate(proba)}
    return result


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "project": "Data Classification Using AI",
        "description": "REST API serving a trained wine-cultivar classification model.",
        "deployed_model": best_model_name,
        "endpoints": ["/health", "/model-info", "/predict [POST]", "/predict-batch [POST]"],
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/model-info", methods=["GET"])
def model_info():
    return jsonify({
        "deployed_model": best_model_name,
        "required_features": feature_cols,
        "n_features": len(feature_cols),
        "n_classes": len(CLASS_LABELS),
        "class_labels": CLASS_LABELS,
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body."}), 400
    try:
        result = make_prediction(data)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"Internal error: {e}"}), 500


@app.route("/predict-batch", methods=["POST"])
def predict_batch():
    data = request.get_json(force=True, silent=True)
    if not isinstance(data, list):
        return jsonify({"error": "Body must be a JSON list of feature objects."}), 400
    try:
        results = [make_prediction(record) for record in data]
        return jsonify({"predictions": results, "count": len(results)}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"Internal error: {e}"}), 500


if __name__ == "__main__":
    print(f"Deployed model: {best_model_name}")
    print(f"Required features ({len(feature_cols)}):", feature_cols)
    app.run(debug=True, host="127.0.0.1", port=5000)
