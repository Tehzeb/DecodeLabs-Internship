"""
main.py
=========
Single entry point that runs the ENTIRE Data Classification Using AI
pipeline end-to-end:

    1. Load raw data            -> src/data_loader.py
    2. Clean / split / scale    -> src/preprocessing.py
    3. Train & tune 7-8 models  -> src/train_models.py
    4. Evaluate & compare       -> src/evaluate.py
    5. Persist best model       -> models/best_model.pkl

Run from the project root:

    python main.py

After this completes, launch the GUI demo with:

    streamlit run app/streamlit_app.py

or the REST API with:

    python app/flask_app.py
"""

import sys
import time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "src"))

from data_loader import load_raw_dataset, save_raw_dataset          # noqa: E402
from preprocessing import run_preprocessing_pipeline                 # noqa: E402
from train_models import train_all_models, save_models               # noqa: E402
from evaluate import run_full_evaluation                             # noqa: E402


def banner(text: str):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def main():
    t0 = time.time()

    banner("STEP 1/4 — LOADING RAW DATA")
    df = load_raw_dataset()
    save_raw_dataset(df)
    print(df.head())

    banner("STEP 2/4 — PREPROCESSING (clean -> split -> scale)")
    X_train, X_test, y_train, y_test, scaler, feature_cols = run_preprocessing_pipeline(df)

    banner("STEP 3/4 — TRAINING & TUNING MODELS (GridSearchCV, 5-fold CV)")
    results = train_all_models(X_train, y_train)
    save_models(results)

    banner("STEP 4/4 — EVALUATION & MODEL SELECTION")
    all_results, comparison_df, best_model_name = run_full_evaluation()

    elapsed = time.time() - t0
    banner("PIPELINE COMPLETE")
    print(comparison_df.round(4).to_string())
    print(f"\nBest model : {best_model_name}")
    print(f"Total time : {elapsed:.1f}s")
    print("\nArtifacts saved in:")
    print("  - models/          (trained models, scaler, best_model.pkl)")
    print("  - data/processed/  (train/test splits)")
    print("  - reports/figures/ (confusion matrices, ROC curves, comparison chart)")
    print("\nNext steps:")
    print("  streamlit run app/streamlit_app.py   # interactive GUI demo")
    print("  python app/flask_app.py              # REST API for deployment")


if __name__ == "__main__":
    main()
