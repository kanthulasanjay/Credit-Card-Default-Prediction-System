# 💳 Credit Card Default Prediction

A machine learning web app that predicts whether a credit card customer is likely to **default on their next payment**, built with **Streamlit** and **scikit-learn**.

The app takes in a customer's credit limit, demographics, repayment history, and billing/payment amounts, then returns a default risk prediction along with probability scores.

---

## 📁 Project Structure

```
.
├── app.py                # Streamlit web application
├── Model.pkl              # Trained ML model (pickled)
├── SPRINT.ipynb           # Full data science workflow: EDA, preprocessing, model training & tuning
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🚀 Features

- Interactive sidebar for customer profile (credit limit, gender, education, marriage, age)
- Sliders for the last 6 months of repayment status (`PAY_0`–`PAY_6`)
- Inputs for bill amounts and previous payment amounts over 6 months
- Live preview of the input data and inferred data types before prediction
- One-click prediction with:
  - Predicted class (Default / No Default)
  - Default probability and safe probability
  - Visual risk banner (green = safe, red = risk)

---

## 🧠 Model

The model was developed in `SPRINT.ipynb` following a full ML pipeline:

1. **Data Cleaning** – missing value imputation, duplicate removal, column standardization
2. **EDA** – univariate, bivariate, and multivariate analysis (distributions, correlations, pairplots)
3. **Outlier Detection** – IQR-based analysis
4. **Feature Encoding** – label encoding of the target, ordinal encoding of categorical features
5. **Feature Scaling** – standardization of numerical features via `ColumnTransformer`
6. **Model Comparison** – Logistic Regression, Decision Tree, Random Forest, SVM, and Naive Bayes were trained and evaluated on accuracy, precision, recall, and F1-score
7. **Hyperparameter Tuning** – `RandomizedSearchCV` across the candidate models/pipelines
8. **Validation** – train/test split plus K-Fold cross-validation to check for overfitting
9. **Export** – the best estimator is serialized to `Model.pkl` (and `best_model.pkl`) with `joblib`/`pickle`

The final saved model expects the following input columns:

| Column | Description |
|---|---|
| `id` | Customer identifier |
| `limit_bal` | Credit limit assigned to the customer |
| `sex` | Gender (`M` / `F`) |
| `education` | Education level |
| `marriage` | Marital status |
| `age` | Customer age |
| `pay_0`, `pay_2`–`pay_6` | Repayment status for the last 6 months |
| `bill_amt1`–`bill_amt6` | Statement balance for the last 6 months |
| `pay_amt1`–`pay_amt6` | Amount paid for the last 6 months |

---

## 🛠️ Installation
1. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ Usage

Make sure `Model.pkl` is in the same directory as `app.py`, then run:

```bash
streamlit run app.py
```

This will open the app in your browser (default: `http://localhost:8501`).

**Steps in the app:**
1. Fill in the customer's profile in the sidebar (credit limit, gender, education, marriage, age).
2. Set repayment status, bill amounts, and payment amounts for the last 6 months in the main panel.
3. Review the input summary and data types in the expandable sections.
4. Click **🔍 Predict Default Risk** to view the prediction, probabilities, and risk banner.

---

## 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn==1.6.1
joblib
```

> ⚠️ The `scikit-learn` version should match the version used to train `Model.pkl` to avoid unpickling/compatibility issues.

---

## 📝 Notes

- The dataset used for training is a Credit Card Defaulter Prediction dataset with features such as credit limit, demographics, repayment status, bill amounts, and payment amounts over 6 months.
- `SPRINT.ipynb` contains the complete exploratory and modeling workflow if you want to retrain or extend the model.
- Retraining a new model will require re-saving it as `Model.pkl` in the project root for `app.py` to pick it up.

---

