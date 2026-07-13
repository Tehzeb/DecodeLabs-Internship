"""
train_models.py
------------------
Trains and hyperparameter-tunes multiple classification algorithms on
the processed Wine dataset, so their performance can be objectively
compared (as requested for an "advanced / multi-model" project).

Models included
----------------
1. Logistic Regression        (linear baseline)
2. K-Nearest Neighbours        (instance-based)
3. Support Vector Machine      (kernel-based, margin classifier)
4. Decision Tree                (interpretable, non-linear)
5. Random Forest                (bagging ensemble)
6. Gradient Boosting            (boosting ensemble)
7. XGBoost                      (state-of-the-art boosting, optional)
8. Multi-Layer Perceptron       (neural network)

Each model is tuned with GridSearchCV (5-fold stratified CV) over a
small, sensible hyperparameter grid, then evaluated on the held-out
test set in evaluate.py.
"""

from pathlib import Path
import json
import logging
import time

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"

try:
    from xgboost import XGBClassifier
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logger.warning(
        "xgboost is not installed — it will be skipped. "
        "Run 'pip install xgboost' to include it in the comparison."
    )


def get_model_grid() -> dict:
    """
    Define each model together with a small hyperparameter grid for
    GridSearchCV. Grids are intentionally compact so the whole
    pipeline trains quickly, but cover the parameters that matter most.
    """
    grid = {
        "Logistic Regression": {
            "estimator": LogisticRegression(max_iter=5000, random_state=42),
            "params": {
                "C": [0.01, 0.1, 1, 10],
                "solver": ["lbfgs"],
            },
        },
        "K-Nearest Neighbors": {
            "estimator": KNeighborsClassifier(),
            "params": {
                "n_neighbors": [3, 5, 7, 9],
                "weights": ["uniform", "distance"],
            },
        },
        "Support Vector Machine": {
            "estimator": SVC(probability=True, random_state=42),
            "params": {
                "C": [0.1, 1, 10],
                "kernel": ["linear", "rbf"],
                "gamma": ["scale"],
            },
        },
        "Decision Tree": {
            "estimator": DecisionTreeClassifier(random_state=42),
            "params": {
                "max_depth": [3, 5, 7, None],
                "min_samples_split": [2, 4, 6],
            },
        },
        "Random Forest": {
            "estimator": RandomForestClassifier(random_state=42),
            "params": {
                "n_estimators": [100, 200],
                "max_depth": [None, 5, 10],
                "min_samples_split": [2, 4],
            },
        },
        "Gradient Boosting": {
            "estimator": GradientBoostingClassifier(random_state=42),
            "params": {
                "n_estimators": [100, 200],
                "learning_rate": [0.05, 0.1],
                "max_depth": [2, 3],
            },
        },
        "Neural Network (MLP)": {
            "estimator": MLPClassifier(max_iter=2000, random_state=42),
            "params": {
                "hidden_layer_sizes": [(32,), (64, 32)],
                "alpha": [0.0001, 0.001],
                "activation": ["relu"],
            },
        },
    }

    if XGBOOST_AVAILABLE:
        grid["XGBoost"] = {
            "estimator": XGBClassifier(
                random_state=42, eval_metric="mlogloss", use_label_encoder=False
            ),
            "params": {
                "n_estimators": [100, 200],
                "max_depth": [3, 5],
                "learning_rate": [0.05, 0.1],
            },
        }

    return grid


def train_all_models(X_train, y_train, cv_folds: int = 5) -> dict:
    """
    Run GridSearchCV for every model in the grid and return the fitted
    best estimators along with their best CV score and training time.
    """
    cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)
    results = {}

    for name, spec in get_model_grid().items():
        logger.info("Training & tuning: %s ...", name)
        start = time.time()

        search = GridSearchCV(
            estimator=spec["estimator"],
            param_grid=spec["params"],
            cv=cv,
            scoring="accuracy",
            n_jobs=-1,
        )
        search.fit(X_train, y_train)
        elapsed = time.time() - start

        results[name] = {
            "best_estimator": search.best_estimator_,
            "best_params": search.best_params_,
            "best_cv_accuracy": search.best_score_,
            "train_time_sec": round(elapsed, 3),
        }
        logger.info(
            "  -> best CV accuracy: %.4f | best params: %s | time: %.2fs",
            search.best_score_, search.best_params_, elapsed,
        )

    return results


def save_models(results: dict):
    """Persist every tuned model to disk and write a summary JSON."""
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    summary = {}

    for name, res in results.items():
        filename = name.lower().replace(" ", "_").replace("(", "").replace(")", "") + ".pkl"
        path = MODELS_DIR / filename
        joblib.dump(res["best_estimator"], path)

        summary[name] = {
            "file": filename,
            "best_params": res["best_params"],
            "best_cv_accuracy": res["best_cv_accuracy"],
            "train_time_sec": res["train_time_sec"],
        }

    with open(MODELS_DIR / "training_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    logger.info("All models + training_summary.json saved to '%s'.", MODELS_DIR)
    return summary


if __name__ == "__main__":
    X_train = pd.read_csv(PROCESSED_DIR / "X_train.csv")
    y_train = pd.read_csv(PROCESSED_DIR / "y_train.csv").squeeze()

    training_results = train_all_models(X_train, y_train)
    save_models(training_results)
