# 🍷 Data Classification Using AI
### Multi-Model Machine Learning Pipeline for Tabular Data Classification

**Internship Project — Artificial Intelligence Track**

---

## 1. Project Overview

This project implements a complete, production-style pipeline that classifies
wine samples into one of **three cultivars** based on **13 chemical/physical
properties** obtained through chemical analysis (the *Wine Recognition
Dataset*, UCI Machine Learning Repository).

It demonstrates the full AI project lifecycle expected at a professional
level:

| Stage | What's implemented |
|---|---|
| **Data Acquisition** | Reproducible loading of a well-known public dataset |
| **EDA** | Two Jupyter notebooks — distribution analysis, correlation, outliers |
| **Preprocessing** | Cleaning, stratified train/test split, feature scaling |
| **Modeling** | **7–8 algorithms** trained & hyperparameter-tuned with `GridSearchCV` |
| **Evaluation** | Accuracy, precision, recall, F1, confusion matrices, ROC-AUC, feature importance |
| **Deployment** | Interactive **Streamlit GUI** + a **Flask REST API** |
| **Engineering practice** | Modular `src/` code, logging, unit tests, `requirements.txt`, this README |

---

## 2. Dataset

**Wine Recognition Dataset** (a.k.a. "Wine" dataset), UCI Machine Learning
Repository, bundled with scikit-learn (`sklearn.datasets.load_wine`).

- **178 samples**, no missing values, no duplicates
- **13 numeric features**: alcohol, malic acid, ash, alcalinity of ash,
  magnesium, total phenols, flavanoids, nonflavanoid phenols,
  proanthocyanins, color intensity, hue, OD280/OD315 of diluted wines, proline
- **3 target classes**: three different cultivars (grape varieties) of wine
  grown in the same region of Italy
- Chosen because it is a genuine, respected tabular multi-class benchmark
  dataset with real chemical/industrial relevance — not a toy binary problem.

---

## 3. Project Structure

```
DataClassificationAI/
├── data/
│   ├── raw/                    # original dataset (CSV)
│   └── processed/              # train/test splits after preprocessing
├── notebooks/
│   ├── 01_EDA_and_Preprocessing.ipynb
│   └── 02_Model_Training_Evaluation.ipynb
├── src/
│   ├── data_loader.py          # dataset acquisition
│   ├── preprocessing.py        # cleaning, split, scaling
│   ├── train_models.py         # multi-model training + GridSearchCV tuning
│   └── evaluate.py             # metrics, confusion matrices, ROC, importance
├── models/                     # saved .pkl models + scaler (generated)
├── app/
│   ├── streamlit_app.py        # interactive GUI (live + batch prediction)
│   └── flask_app.py            # REST API for deployment
├── reports/
│   ├── figures/                # generated charts (created by evaluate.py)
│   └── Project_Report.docx     # full written report
├── tests/
│   └── test_pipeline.py        # unit tests (pytest)
├── main.py                     # runs the ENTIRE pipeline end-to-end
├── requirements.txt
└── README.md                   # you are here
```

---

## 4. Models Trained & Compared

| # | Model | Type |
|---|---|---|
| 1 | Logistic Regression | Linear baseline |
| 2 | K-Nearest Neighbors | Instance-based |
| 3 | Support Vector Machine (RBF/linear) | Kernel-based margin classifier |
| 4 | Decision Tree | Interpretable non-linear |
| 5 | Random Forest | Bagging ensemble |
| 6 | Gradient Boosting | Boosting ensemble |
| 7 | XGBoost *(if installed)* | State-of-the-art boosting |
| 8 | Neural Network (MLP) | Feed-forward neural network |

Every model is tuned with **5-fold stratified `GridSearchCV`**, then compared
on a held-out **20% test set** using accuracy, macro-precision, macro-recall
and macro-F1. The best model on the test set is automatically selected and
saved as `models/best_model.pkl` for deployment.

---

## 5. Setup Instructions — Windows 11 + VS Code

### Step 1 — Install prerequisites
1. Install **Python 3.10+** from [python.org](https://www.python.org/downloads/)
   — during installation, tick **"Add Python to PATH"**.
2. Install **VS Code** from [code.visualstudio.com](https://code.visualstudio.com/).
3. In VS Code, install these extensions (Extensions icon on the left sidebar):
   - **Python** (Microsoft)
   - **Jupyter** (Microsoft)

### Step 2 — Open the project
1. Extract/copy the `DataClassificationAI` folder anywhere, e.g. `C:\Projects\DataClassificationAI`.
2. In VS Code: `File → Open Folder...` → select `DataClassificationAI`.

### Step 3 — Create a virtual environment
Open a terminal in VS Code (`` Ctrl+` ``) and run:

```powershell
python -m venv venv
venv\Scripts\activate
```

You should now see `(venv)` at the start of the terminal prompt. If VS Code
prompts *"Select Interpreter"*, choose the one inside `.\venv\Scripts\python.exe`.

### Step 4 — Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 5 — Run the full pipeline

```powershell
python main.py
```

This single command will: load the data → clean & preprocess it → train and
tune all 7–8 models → evaluate them → save the best model and all charts.
It takes roughly **1–3 minutes** depending on your machine.

### Step 6 — Launch the interactive GUI (optional but recommended)

```powershell
streamlit run app/streamlit_app.py
```

This opens a browser tab where you can move sliders for each chemical
feature and get a live prediction, upload a CSV for batch predictions, and
browse all model performance charts.

### Step 7 — Launch the REST API (optional, for deployment demos)

```powershell
python app/flask_app.py
```

Then, in a second terminal, test it:

```powershell
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d "{\"alcohol\": 13.2, \"malic_acid\": 1.78, \"ash\": 2.14, \"alcalinity_of_ash\": 11.2, \"magnesium\": 100, \"total_phenols\": 2.65, \"flavanoids\": 2.76, \"nonflavanoid_phenols\": 0.26, \"proanthocyanins\": 1.28, \"color_intensity\": 4.38, \"hue\": 1.05, \"od280/od315_of_diluted_wines\": 3.4, \"proline\": 1050}"
```

### Step 8 — Explore the notebooks (optional)
In VS Code, open `notebooks/01_EDA_and_Preprocessing.ipynb`, click **"Select
Kernel"** in the top-right and choose the `venv` interpreter, then run cells
top-to-bottom with `Shift+Enter`.

### Step 9 — Run unit tests (optional)

```powershell
pytest tests/ -v
```

---

## 6. Results Summary

After running `main.py`, a full model comparison table and all charts are
generated in `reports/figures/`. On this dataset, the ensemble and
neural-network models typically achieve **97–100% test accuracy**, comfortably
beating the linear baseline, while remaining fully reproducible via a fixed
`random_state=42` throughout the pipeline.

See `reports/Project_Report.docx` for the full written report with
methodology, results discussion, and conclusions.

---

## 7. Key Engineering Practices Demonstrated

- **Reproducibility**: fixed random seeds, versioned dependencies, saved
  train/test splits and fitted scaler.
- **No data leakage**: the `StandardScaler` is fit only on the training
  split.
- **Stratified sampling**: preserves class balance in train/test splits and
  cross-validation folds — important for the moderately imbalanced classes.
- **Systematic hyperparameter tuning**: `GridSearchCV` with cross-validation
  for every model, not just default parameters.
- **Model-agnostic interpretability**: permutation importance is used as a
  fallback for models without native feature-importance (SVM, KNN, Neural
  Network).
- **Separation of concerns**: data loading, preprocessing, training and
  evaluation are independent, testable modules — not one monolithic script.
- **Two deployment paths**: a human-facing GUI (Streamlit) and a
  machine-facing REST API (Flask), reflecting real-world deployment options.
- **Logging** throughout instead of scattered `print()` statements.
- **Unit tests** validating data integrity and minimum model performance.

---

## 8. Possible Future Extensions

- Add SHAP values for deeper per-prediction explainability.
- Containerize the Flask API with Docker for cloud deployment.
- Add MLflow or Weights & Biases experiment tracking.
- Extend to a larger/streaming dataset with automated retraining.
- Add authentication and rate-limiting to the REST API for production use.

---

## 9. Author's Notes

This project was built as part of an Artificial Intelligence internship,
demonstrating an end-to-end, professional-standard classification pipeline
on structured/tabular data — from raw data to a deployable, interactive
application.
