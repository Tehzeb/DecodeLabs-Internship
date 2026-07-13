"""
evaluate.py
-------------
Evaluates every tuned model on the held-out test set, generates
professional-quality figures (confusion matrices, ROC curves, model
comparison chart, feature importance) and selects/saves the best
overall model for deployment.
"""

from pathlib import Path
import json
import logging

import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc,
)
from sklearn.preprocessing import label_binarize
from sklearn.inspection import permutation_importance

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams["figure.dpi"] = 130

CLASS_NAMES = ["class_0 (Cultivar A)", "class_1 (Cultivar B)", "class_2 (Cultivar C)"]


def load_test_data():
    X_test = pd.read_csv(PROCESSED_DIR / "X_test.csv")
    y_test = pd.read_csv(PROCESSED_DIR / "y_test.csv").squeeze()
    return X_test, y_test


def load_trained_models() -> dict:
    with open(MODELS_DIR / "training_summary.json") as f:
        summary = json.load(f)
    models = {name: joblib.load(MODELS_DIR / info["file"]) for name, info in summary.items()}
    return models, summary


def evaluate_model(name, model, X_test, y_test) -> dict:
    y_pred = model.predict(X_test)
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision_macro": precision_score(y_test, y_pred, average="macro"),
        "recall_macro": recall_score(y_test, y_pred, average="macro"),
        "f1_macro": f1_score(y_test, y_pred, average="macro"),
    }
    report = classification_report(y_test, y_pred, target_names=CLASS_NAMES, output_dict=True)
    cm = confusion_matrix(y_test, y_pred)
    return {"metrics": metrics, "report": report, "confusion_matrix": cm, "y_pred": y_pred}


def plot_confusion_matrix(name, cm, save_path):
    plt.figure(figsize=(5.5, 4.5))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES, cbar=False,
    )
    plt.title(f"Confusion Matrix — {name}", fontsize=12, fontweight="bold")
    plt.ylabel("Actual Class")
    plt.xlabel("Predicted Class")
    plt.xticks(rotation=20, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()


def plot_roc_curves(name, model, X_test, y_test, save_path):
    """One-vs-rest ROC curve for each of the 3 classes."""
    y_test_bin = label_binarize(y_test, classes=[0, 1, 2])
    if not hasattr(model, "predict_proba"):
        return False

    y_score = model.predict_proba(X_test)

    plt.figure(figsize=(6, 5))
    colors = ["#2563eb", "#dc2626", "#16a34a"]
    for i in range(3):
        fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_score[:, i])
        roc_auc = auc(fpr, tpr)
        plt.plot(fpr, tpr, color=colors[i], lw=2,
                 label=f"{CLASS_NAMES[i]} (AUC = {roc_auc:.3f})")

    plt.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.5)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"ROC Curves (One-vs-Rest) — {name}", fontsize=12, fontweight="bold")
    plt.legend(loc="lower right", fontsize=8)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    return True


def plot_model_comparison(all_metrics: dict, save_path):
    df = pd.DataFrame({name: m["metrics"] for name, m in all_metrics.items()}).T
    df = df.sort_values("accuracy", ascending=False)

    ax = df.plot(
        kind="bar", figsize=(11, 6),
        color=["#2563eb", "#f59e0b", "#16a34a", "#dc2626"],
        width=0.75,
    )
    plt.title("Model Comparison — Test Set Performance", fontsize=13, fontweight="bold")
    plt.ylabel("Score")
    plt.xlabel("Model")
    plt.xticks(rotation=30, ha="right")
    plt.ylim(0, 1.05)
    plt.legend(title="Metric", bbox_to_anchor=(1.02, 1), loc="upper left")
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", fontsize=7, rotation=90, padding=2)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    return df


def plot_feature_importance(name, model, feature_names, save_path, X_test=None, y_test=None):
    """
    Plot feature importance for tree-based models, coefficients for linear
    models, or — for models with neither (e.g. SVM-RBF, KNN, Neural Nets) —
    fall back to model-agnostic permutation importance on the test set.
    """
    importances = None
    method_label = "Importance"

    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
    elif hasattr(model, "coef_"):
        importances = np.mean(np.abs(model.coef_), axis=0)
    elif X_test is not None and y_test is not None:
        logger.info("  '%s' has no native importances — using permutation importance.", name)
        perm = permutation_importance(model, X_test, y_test, n_repeats=20, random_state=42, n_jobs=-1)
        importances = perm.importances_mean
        method_label = "Permutation Importance"

    if importances is None:
        return False

    imp_df = pd.DataFrame({"feature": feature_names, "importance": importances})
    imp_df = imp_df.sort_values("importance", ascending=True).tail(13)

    plt.figure(figsize=(7, 6))
    plt.barh(imp_df["feature"], imp_df["importance"], color="#2563eb")
    plt.title(f"{method_label} — {name}", fontsize=12, fontweight="bold")
    plt.xlabel(method_label)
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches="tight")
    plt.close()
    return True


def run_full_evaluation():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    X_test, y_test = load_test_data()
    models, summary = load_trained_models()
    feature_names = joblib.load(MODELS_DIR / "feature_columns.pkl")

    all_results = {}
    for name, model in models.items():
        logger.info("Evaluating: %s", name)
        result = evaluate_model(name, model, X_test, y_test)
        all_results[name] = result

        safe_name = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
        plot_confusion_matrix(name, result["confusion_matrix"], FIGURES_DIR / f"cm_{safe_name}.png")
        plot_roc_curves(name, model, X_test, y_test, FIGURES_DIR / f"roc_{safe_name}.png")

    comparison_df = plot_model_comparison(all_results, FIGURES_DIR / "model_comparison.png")
    logger.info("\n%s", comparison_df.round(4).to_string())

    best_model_name = comparison_df["accuracy"].idxmax()
    best_model = models[best_model_name]
    logger.info("Best model on test set: %s (accuracy=%.4f)", best_model_name, comparison_df.loc[best_model_name, "accuracy"])

    plot_feature_importance(
        best_model_name, best_model, feature_names,
        FIGURES_DIR / "feature_importance_best_model.png",
        X_test=X_test, y_test=y_test,
    )

    joblib.dump(best_model, MODELS_DIR / "best_model.pkl")
    with open(MODELS_DIR / "best_model_name.json", "w") as f:
        json.dump({"best_model": best_model_name}, f, indent=2)

    final_report = {
        name: {
            "metrics": {k: round(v, 4) for k, v in res["metrics"].items()},
        }
        for name, res in all_results.items()
    }
    with open(FIGURES_DIR.parent / "evaluation_report.json", "w") as f:
        json.dump(final_report, f, indent=2)

    logger.info("Evaluation complete. Figures saved to '%s'.", FIGURES_DIR)
    return all_results, comparison_df, best_model_name


if __name__ == "__main__":
    run_full_evaluation()
