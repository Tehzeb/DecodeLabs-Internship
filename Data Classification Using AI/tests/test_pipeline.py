"""
test_pipeline.py
-------------------
Basic unit tests validating the data loading, preprocessing and model
artifacts. Run with:

    pytest tests/ -v

(from the project root, after main.py has been run at least once so
that models/ and data/processed/ are populated).
"""

from pathlib import Path
import sys

import joblib
import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT / "src"))

from data_loader import load_raw_dataset          # noqa: E402
from preprocessing import clean_data, split_features_target  # noqa: E402

MODELS_DIR = PROJECT_ROOT / "models"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def test_dataset_loads_correctly():
    df = load_raw_dataset()
    assert df.shape[0] == 178
    assert "target" in df.columns
    assert df["target"].nunique() == 3


def test_no_missing_values_after_cleaning():
    df = load_raw_dataset()
    df_clean = clean_data(df)
    assert df_clean.isnull().sum().sum() == 0


def test_feature_target_split_shapes():
    df = load_raw_dataset()
    X, y, feature_cols = split_features_target(df)
    assert X.shape[1] == 13
    assert len(feature_cols) == 13
    assert X.shape[0] == y.shape[0]


@pytest.mark.skipif(
    not (PROCESSED_DIR / "X_test.csv").exists(),
    reason="Run 'python main.py' first to generate processed data.",
)
def test_processed_split_is_stratified():
    y_train = pd.read_csv(PROCESSED_DIR / "y_train.csv").squeeze()
    y_test = pd.read_csv(PROCESSED_DIR / "y_test.csv").squeeze()
    train_ratios = y_train.value_counts(normalize=True).sort_index()
    test_ratios = y_test.value_counts(normalize=True).sort_index()
    assert (abs(train_ratios - test_ratios) < 0.1).all()


@pytest.mark.skipif(
    not (MODELS_DIR / "best_model.pkl").exists(),
    reason="Run 'python main.py' first to train models.",
)
def test_best_model_predicts_valid_classes():
    model = joblib.load(MODELS_DIR / "best_model.pkl")
    X_test = pd.read_csv(PROCESSED_DIR / "X_test.csv")
    preds = model.predict(X_test)
    assert set(preds).issubset({0, 1, 2})
    assert len(preds) == len(X_test)


@pytest.mark.skipif(
    not (MODELS_DIR / "training_summary.json").exists(),
    reason="Run 'python main.py' first to train models.",
)
def test_all_models_meet_minimum_accuracy():
    import json
    with open(MODELS_DIR / "training_summary.json") as f:
        summary = json.load(f)
    for name, info in summary.items():
        assert info["best_cv_accuracy"] > 0.85, f"{name} underperforms threshold"
