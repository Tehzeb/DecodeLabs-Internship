"""
data_loader.py
----------------
Handles acquisition of the raw dataset used for this project.

Dataset : Wine Recognition Dataset (UCI Machine Learning Repository)
Source  : Forina, M. et al. PARVUS - An Extendible Package for Data
          Exploration, Classification and Correlation. Institute of
          Pharmaceutical and Food Analysis and Technologies, Genoa, Italy.
Access  : Bundled with scikit-learn (sklearn.datasets.load_wine), which
          mirrors the original UCI Machine Learning Repository release.

Description
-----------
The dataset is the result of a chemical analysis of wines grown in the
same region in Italy but derived from three different cultivars (classes).
13 continuous features describe the quantities of various constituents
found in each of the three types of wine (e.g. alcohol content, malic
acid, flavanoids, color intensity, proline, etc.).

Author : AI/ML Internship Project - Data Classification Using AI
"""

from pathlib import Path
import logging

import pandas as pd
from sklearn.datasets import load_wine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

RAW_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "raw" / "wine_dataset.csv"


def load_raw_dataset() -> pd.DataFrame:
    """
    Load the Wine Recognition dataset into a single tidy DataFrame.

    Returns
    -------
    pd.DataFrame
        Feature columns (13) + 'target' (0/1/2) + 'target_name'
        (class_0 / class_1 / class_2 cultivar labels).
    """
    logger.info("Loading Wine Recognition dataset from scikit-learn ...")
    bunch = load_wine(as_frame=True)

    df = bunch.frame.copy()
    df["target_name"] = df["target"].map(dict(enumerate(bunch.target_names)))

    logger.info(
        "Dataset loaded successfully: %d rows, %d columns, %d classes.",
        df.shape[0],
        df.shape[1],
        df["target"].nunique(),
    )
    return df


def save_raw_dataset(df: pd.DataFrame, path: Path = RAW_DATA_PATH) -> Path:
    """Persist the raw dataset to disk as CSV for reproducibility."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logger.info("Raw dataset saved to: %s", path)
    return path


def get_feature_and_target_info() -> dict:
    """Return metadata describing the dataset (used in reports / GUI)."""
    bunch = load_wine()
    return {
        "feature_names": list(bunch.feature_names),
        "target_names": list(bunch.target_names),
        "n_samples": bunch.data.shape[0],
        "n_features": bunch.data.shape[1],
        "n_classes": len(bunch.target_names),
        "description": bunch.DESCR,
    }


if __name__ == "__main__":
    dataframe = load_raw_dataset()
    save_raw_dataset(dataframe)
    print(dataframe.head())
    print("\nClass distribution:\n", dataframe["target_name"].value_counts())
