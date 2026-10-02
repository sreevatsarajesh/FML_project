# Explainable Probabilistic Phishing Website Detection

A machine-learning-based phishing website detection system that analyzes numerical characteristics derived from URLs and classifies websites as **legitimate** or **phishing**.

The project combines a machine-learning research pipeline with a Flask-based web application for real-time URL analysis.

---

## Project Overview

The project uses supervised machine learning to detect potentially phishing websites from URL-derived features.

The machine-learning side of the project focuses on:

* Dataset inspection
* Data preprocessing
* Exploratory analysis
* Feature selection
* Model training
* Model evaluation
* Explainability

The application side focuses on:

* URL input
* URL feature extraction
* Prediction
* Probability output
* Risk scoring
* Explanation display
* Flask backend
* Web interface

The project evaluates:

* Logistic Regression
* Decision Tree
* Random Forest

The project synopsis describes the same overall methodology, including preprocessing, feature analysis, probabilistic prediction, risk scoring, explainability, and model evaluation.

---

# Dataset

The project uses the **Web Page Phishing Dataset** by Daniel Fernando from Kaggle.

Dataset:

[Web Page Phishing Dataset — Kaggle](https://www.kaggle.com/datasets/danielfernandon/web-page-phishing-dataset?resource=download)

The project synopsis identifies this dataset as containing 100,007 instances of URL-derived numerical feature vectors for phishing detection.

The dataset is used for:

* Dataset inspection
* Preprocessing
* Exploratory analysis
* Feature selection
* Model training
* Model evaluation
* Explainability

---

# Project Architecture

```text
FML_project/
│
├── app/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
│
├── data/
│   └── phishing_detection/
│       └── phishing.csv
│
├── notebooks/
│   ├── 01_dataset_inspection.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_exploratory_analysis.ipynb
│   ├── 04_feature_selection.ipynb
│   ├── 05_model_training.ipynb
│   ├── 06_model_evaluation.ipynb
│   └── 07_explainability.ipynb
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py
│   ├── feature_selection.py
│   ├── train_models.py
│   ├── evaluate_models.py
│   ├── explain.py
│   ├── feature_extraction.py
│   ├── predict.py
│   └── risk_scoring.py
│
├── models/
│   └── trained model files
│
├── results/
│   ├── metrics/
│   └── figures/
│
├── tests/
│
├── config/
│   └── config.yaml
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Team Responsibilities

## Vatsa — ML / Research Workstream

Vatsa is responsible for developing and validating the machine-learning pipeline.

### Dataset Inspection

```text
notebooks/01_dataset_inspection.ipynb
```

Tasks:

* Inspect dataset shape
* Identify columns
* Identify target column
* Inspect data types
* Check missing values
* Check duplicates
* Analyze class distribution
* Understand feature meanings

---

### Data Preprocessing

```text
notebooks/02_data_preprocessing.ipynb
src/preprocessing.py
```

Tasks:

* Clean dataset
* Remove duplicates if required
* Handle missing values
* Separate features and target
* Create train/test split
* Apply required preprocessing
* Save preprocessing information where required

---

### Exploratory Analysis

```text
notebooks/03_exploratory_analysis.ipynb
```

Tasks:

* Class distribution
* Feature distributions
* Correlation analysis
* Outlier analysis
* Relationships between features and target

---

### Feature Selection

```text
notebooks/04_feature_selection.ipynb
src/feature_selection.py
```

Tasks:

* Determine relevant features
* Identify redundant features
* Determine final feature set
* Establish exact feature order

The final feature order is particularly important because the application must generate features in exactly the same order expected by the trained model.

---

### Model Training

```text
notebooks/05_model_training.ipynb
src/train_models.py
```

Models:

* Logistic Regression
* Decision Tree
* Random Forest

The notebooks are used for experimentation and model development.

Final trained models may be exported to:

```text
models/
```

For example:

```text
models/
├── logistic_regression.pkl
├── decision_tree.pkl
├── random_forest.pkl
└── scaler.pkl
```

---

### Model Evaluation

```text
notebooks/06_model_evaluation.ipynb
src/evaluate_models.py
```

Metrics:

* Accuracy
* Precision
* Recall
* F1-score
* ROC-AUC
* Confusion matrix

Results are stored under:

```text
results/
├── metrics/
└── figures/
```

---

### Explainability

```text
notebooks/07_explainability.ipynb
src/explain.py
```

Tasks:

* Feature importance
* Logistic Regression coefficients
* Important URL characteristics
* Prediction explanations

---

# You — Application / System Workstream

The application side connects the trained machine-learning system to a real URL.

## Frontend

```text
app/templates/index.html
app/static/style.css
app/static/script.js
```

Responsibilities:

* URL input
* Analyze button
* Result display
* Probability display
* Risk-level display
* Explanation display
* Error handling
* Responsive UI

---

## URL Feature Extraction

```text
src/feature_extraction.py
```

This module accepts a raw URL and generates the same feature representation expected by the trained model.

Example:

```text
https://example.com/login
        │
        ▼
Feature Extraction
        │
        ▼
[url_length, n_dots, n_hyphens, ...]
        │
        ▼
Model-compatible feature vector
```

This module will be finalized only after the ML workstream provides:

* Complete feature list
* Exact feature order
* Target column
* Required preprocessing
* Feature definitions

---

## Prediction Pipeline

```text
src/predict.py
```

The prediction pipeline will eventually perform:

```text
Raw URL
   ↓
Feature Extraction
   ↓
Preprocessing
   ↓
Trained Model
   ↓
Prediction
   ↓
Probability
```

The prediction module should remain independent of Flask so it can be tested separately.

---

## Risk Scoring

```text
src/risk_scoring.py
```

The module converts the model probability into an application-level risk score.

```text
Model Probability
       ↓
Risk Score
       ↓
Risk Level
```

The exact thresholds will be finalized during development.

---

## Flask Backend

```text
app/app.py
```

Responsibilities:

* Receive URL
* Validate request
* Call feature extraction
* Call prediction pipeline
* Call risk scoring
* Obtain explanation
* Return result to frontend

The Flask layer should not contain model-training logic.

---

# Complete Application Flow

```text
User
 │
 │ enters URL
 ▼
Frontend
 │
 │ POST request
 ▼
Flask
 │
 ▼
Feature Extraction
 │
 ▼
Preprocessing
 │
 ▼
Trained ML Model
 │
 ├── Logistic Regression
 ├── Decision Tree
 └── Random Forest
 │
 ▼
Prediction + Probability
 │
 ▼
Risk Scoring
 │
 ▼
Explanation
 │
 ▼
Flask Response
 │
 ▼
Frontend
 │
 ▼
Result
```

---

# Current Development Plan

The project is being developed in stages.

## Stage 1 — ML Foundation

**Vatsa**

```text
01_dataset_inspection.ipynb
        ↓
02_data_preprocessing.ipynb
        ↓
03_exploratory_analysis.ipynb
        ↓
04_feature_selection.ipynb
```

The key output of this stage is the finalized model input specification.

---

## Stage 2 — Backend Skeleton

**Application/System workstream**

While Vatsa works on preprocessing and feature analysis, the application side can be developed independently.

Initial work:

```text
app/app.py
src/predict.py
src/risk_scoring.py
tests/
index.html
style.css
script.js
```

At this stage, placeholder prediction data can be used to verify frontend/backend communication.

---

## Stage 3 — Model Development

**Vatsa**

```text
05_model_training.ipynb
        ↓
06_model_evaluation.ipynb
        ↓
07_explainability.ipynb
```

Models are trained and evaluated in Jupyter notebooks before being exported for application use.

---

## Stage 4 — Integration

Once the ML specification is finalized:

```text
Raw URL
   ↓
feature_extraction.py
   ↓
preprocessing.py
   ↓
trained model
   ↓
predict.py
   ↓
risk_scoring.py
   ↓
explain.py
   ↓
Flask
   ↓
Frontend
```

Initially, at least one trained model will be integrated into the application before expanding the system to the remaining models.

---

# Current Milestone

The immediate development goal is:

### Vatsa

Complete:

* Dataset inspection
* Data preprocessing
* Initial feature analysis
* Establish the final model input format

### Application/System

Complete:

* Flask backend skeleton
* Frontend structure
* Prediction pipeline skeleton
* Risk-scoring skeleton
* Basic tests

### Integration checkpoint

After the ML preprocessing/input format is finalized:

```text
Feature Specification
        ↓
Feature Extraction
        ↓
Prediction Pipeline
        ↓
ONE trained model
        ↓
Probability
        ↓
Risk Score
        ↓
Frontend
```

This provides an end-to-end working prototype before integrating the remaining models.

---

# Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Application

From the project root:

```bash
python -m app.app
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

# Testing

Run:

```bash
pytest
```

Tests cover the prediction pipeline, risk scoring, model integration, and application components as they are implemented.

---

# Limitations

The system is an academic machine-learning project.

A prediction is probabilistic and may result in false positives or false negatives. URL-derived features alone may also fail to capture every characteristic of a malicious website.

The risk score is an interpretation of model output and should not be treated as an absolute security measurement.

---

# Dataset and References

1. Daniel Fernando, **Web Page Phishing Dataset**, Kaggle.
2. Aurélien Géron, *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*.
3. Max Kuhn and Kjell Johnson, *Applied Predictive Modeling*.
4. Leo Breiman, *Random Forests*.
5. Trevor Hastie, Robert Tibshirani, and Jerome Friedman, *The Elements of Statistical Learning*.

---

# Authors

**Dheeman Thakur**   - **240957082**<br>
**Sreevatsa Rajesh** - **240957021**<br>
**Arjun Sriram**     - **240957034**

Department of Computer Science
Manipal Institute of Technology, Manipal
