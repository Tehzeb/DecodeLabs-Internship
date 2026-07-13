"""
preprocessing.py
------------------
Data cleaning, feature scaling and train/test splitting utilities.

The Wine Recognition dataset has no missing values by construction, but
this module is written defensively (as a real-world project would be)
so it gracefully handles missing values, duplicate rows and outliers if
they were ever present in a refreshed data pull.
"""

from pathlib import Path
import logging

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic data-quality pass: drop exact duplicates, report/handle
    missing values, and enforce numeric dtypes on feature columns.
    """
    n_before = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    n_after = len(df)
    if n_before != n_after:
        logger.info("Removed %d duplicate rows.", n_before - n_after)

    missing = df.isnull().sum()
    if missing.sum() > 0:
        logger.warning("Missing values detected:\n%s", missing[missing > 0])
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        logger.info("Missing numeric values imputed with column median.")
    else:
        logger.info("No missing values found — dataset is clean.")

    return df


def split_features_target(df: pd.DataFrame):
    """Separate feature matrix X from target vector y."""
    feature_cols = [c for c in df.columns if c not in ("target", "target_name")]
    X = df[feature_cols].copy()
    y = df["target"].copy()
    return X, y, feature_cols


def train_test_splitter(X, y, test_size: float = 0.2, random_state: int = 42):
    """
    Stratified train/test split — stratification preserves the class
    balance of the three wine cultivars in both splits, which matters
    for a modestly sized (178-row) multi-class dataset.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    logger.info(
        "Train/test split -> train: %d rows, test: %d rows (stratified, test_size=%.0f%%)",
        len(X_train), len(X_test), test_size * 100,
    )
    return X_train, X_test, y_train, y_test


def scale_features(X_train, X_test):
    """
    Standardize features (zero mean, unit variance). Fit only on the
    training split to avoid data leakage from the test set.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)

    return X_train_scaled, X_test_scaled, scaler


def save_processed_artifacts(X_train, X_test, y_train, y_test, scaler, feature_cols):
    """Persist processed splits and the fitted scaler for reproducibility / deployment."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    X_train.to_csv(PROCESSED_DIR / "X_train.csv", index=False)
    X_test.to_csv(PROCESSED_DIR / "X_test.csv", index=False)
    y_train.to_csv(PROCESSED_DIR / "y_train.csv", index=False)
    y_test.to_csv(PROCESSED_DIR / "y_test.csv", index=False)

    joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
    joblib.dump(feature_cols, MODELS_DIR / "feature_columns.pkl")

    logger.info("Processed data + scaler saved to '%s' and '%s'.", PROCESSED_DIR, MODELS_DIR)


def run_preprocessing_pipeline(df: pd.DataFrame):
    """End-to-end preprocessing: clean -> split -> scale -> persist."""
    df_clean = clean_data(df)
    X, y, feature_cols = split_features_target(df_clean)
    X_train, X_test, y_train, y_test = train_test_splitter(X, y)
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    save_processed_artifacts(X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_cols)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, feature_cols


if __name__ == "__main__":
    from data_loader import load_raw_dataset

    raw_df = load_raw_dataset()
    run_preprocessing_pipeline(raw_df)
