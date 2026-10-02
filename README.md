# Explainable Probabilistic Phishing Website Detection

A machine-learning-based phishing website detection system that analyzes numerical characteristics derived from URLs and classifies websites as **legitimate** or **phishing**.

The project combines supervised machine learning, feature selection, probabilistic prediction, risk scoring, and model explainability into a single pipeline with a web-based interface.

---

## Project Overview

Phishing websites attempt to deceive users into revealing sensitive information by imitating legitimate websites or services.

Traditional phishing detection approaches often rely on manually maintained blacklists. While useful, blacklist-based approaches can struggle with newly created or previously unseen malicious URLs.

This project explores a feature-based machine learning approach. Numerical characteristics extracted from URLs are used to train classification models that distinguish between legitimate and phishing websites.

The system additionally provides:

* Probabilistic predictions
* Risk scoring
* Feature selection
* Model comparison
* Model evaluation
* Explainability
* A web interface for URL prediction

The project evaluates **Logistic Regression, Decision Tree, and Random Forest** models as described in the project methodology.

---

## Objectives

The primary objectives of the project are:

1. Develop an automated machine-learning system for classifying URLs as legitimate or phishing.
2. Compare multiple supervised classification algorithms.
3. Use preprocessing and feature selection to improve the machine-learning pipeline.
4. Generate probabilistic predictions for detected URLs.
5. Convert prediction probabilities into an interpretable risk score.
6. Provide feature-level explanations for model predictions.
7. Evaluate the models using multiple classification metrics.
8. Integrate the trained prediction pipeline with a web application.

---

## Dataset

The project uses the **Web Page Phishing Dataset** created by **Daniel Fernando** and published on Kaggle.

**Dataset source:**

[Web Page Phishing Dataset — Kaggle](https://www.kaggle.com/datasets/danielfernandon/web-page-phishing-dataset?resource=download&utm_source=chatgpt.com)

The dataset contains numerical features derived from web-page/URL characteristics for phishing detection. The project synopsis identifies the dataset as containing **100,007 instances** of URL-derived numerical feature vectors.

The dataset is used as the basis for:

* Dataset inspection
* Data preprocessing
* Exploratory analysis
* Feature selection
* Model training
* Model evaluation
* Explainability

The dataset should be placed under:

```text
data/phishing_detection/
```

---

## Machine Learning Pipeline

The overall pipeline follows these stages:

```text
Dataset
   │
   ▼
Dataset Inspection
   │
   ▼
Preprocessing
   │
   ▼
Exploratory Analysis
   │
   ▼
Feature Selection
   │
   ▼
Model Training
   │
   ├── Logistic Regression
   ├── Decision Tree
   └── Random Forest
   │
   ▼
Model Evaluation
   │
   ▼
Prediction
   │
   ▼
Risk Scoring
   │
   ▼
Explainability
   │
   ▼
Web Application
```

The project methodology specifically includes data-quality inspection, class-distribution analysis, feature analysis, model training, probabilistic prediction, feature-level explanation, and evaluation using Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrices.

---

## Repository Structure

```text
FML_project/
│
├── data/
│   └── phishing_detection/
│       └── data.csv
│
├── app/
│   ├── app.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
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
│   ├── evaluate_models.py
│   ├── explain.py
│   ├── feature_selection.py
│   ├── predict.py
│   ├── preprocessing.py
│   ├── risk_scoring.py
│   └── train_models.py
│
├── tests/
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Directory Responsibilities

### `data/`

Contains the dataset used for training and evaluation.

```text
data/
└── phishing_detection/
    └── data.csv
```

Large datasets and generated artifacts should generally not be committed unless required by the project.

---

### `notebooks/`

The notebooks document the experimental machine-learning workflow.

| Notebook                        | Purpose                                                          |
| ------------------------------- | ---------------------------------------------------------------- |
| `01_dataset_inspection.ipynb`   | Inspect dataset structure, missing values, duplicates and labels |
| `02_data_preprocessing.ipynb`   | Clean and transform the dataset                                  |
| `03_exploratory_analysis.ipynb` | Analyze distributions, correlations and feature behaviour        |
| `04_feature_selection.ipynb`    | Identify relevant features                                       |
| `05_model_training.ipynb`       | Train the classification models                                  |
| `06_model_evaluation.ipynb`     | Compare model performance                                        |
| `07_explainability.ipynb`       | Analyze model decisions and feature influence                    |

---

### `src/`

Contains reusable Python modules used by the machine-learning pipeline.

#### `preprocessing.py`

Responsible for preparing input data for the models.

Possible responsibilities include:

* Data cleaning
* Handling missing values
* Feature transformations
* Scaling
* Preparing model-compatible feature vectors

#### `feature_selection.py`

Contains the feature-selection logic used to identify relevant URL characteristics.

#### `train_models.py`

Responsible for training the machine-learning models.

Models considered in the project include:

* Logistic Regression
* Decision Tree
* Random Forest

#### `evaluate_models.py`

Contains model evaluation functionality.

Evaluation metrics include:

* Accuracy
* Precision
* Recall
* F1-Score
* ROC-AUC
* Confusion Matrix

#### `predict.py`

Provides the prediction interface used by the application.

The application should call this module rather than implementing machine-learning prediction logic directly inside `app.py`.

#### `risk_scoring.py`

Converts model prediction information/probabilities into an interpretable phishing-risk score.

#### `explain.py`

Provides feature-level information explaining why a prediction was produced.

---

## Web Application

The web application provides a simple interface for submitting a URL and receiving a phishing-detection result.

```text
Browser
   │
   ▼
app/app.py
   │
   ▼
src/predict.py
   │
   ├── preprocessing.py
   ├── trained model
   ├── risk_scoring.py
   └── explain.py
   │
   ▼
Prediction Result
   │
   ▼
HTML Response
```

The Flask application is intentionally kept separate from the machine-learning implementation.

---

## Prediction Flow

A typical prediction request follows this process:

```text
User enters URL
       │
       ▼
Flask application
       │
       ▼
Validate input
       │
       ▼
Extract / construct URL features
       │
       ▼
Preprocess features
       │
       ▼
Load trained model
       │
       ▼
Generate prediction probability
       │
       ▼
Calculate risk score
       │
       ▼
Generate explanation
       │
       ▼
Display result
```

---

## Model Output

The application is intended to expose information such as:

```text
URL: example.com

Prediction: Legitimate

Phishing Probability: 12.4%

Risk Score: 12/100

Explanation:
- Low URL complexity
- Low suspicious-symbol frequency
- No major redirection indicators
```

The exact explanation depends on the implementation of the model and `explain.py`.

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd FML_project
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

From the project root:

```bash
python app/app.py
```

The Flask development server should then provide a local address such as:

```text
http://127.0.0.1:5000
```

Open the address in a browser and submit a URL for analysis.

---

## Testing

Tests are stored in:

```text
tests/
```

Run the test suite using:

```bash
pytest
```

Tests should cover, where applicable:

* URL input validation
* Prediction pipeline
* Risk-score generation
* Invalid input handling
* Application routes
* Model loading
* Prediction output format

---

## Limitations

This system is a machine-learning research/academic project and should not be treated as a complete real-world phishing protection system.

Potential limitations include:

* The model is dependent on the characteristics represented in the training dataset.
* Previously unseen URL patterns may not be represented adequately.
* A machine-learning prediction is probabilistic and can produce false positives or false negatives.
* URL-based numerical features alone cannot capture every property of a website.
* The risk score is an interpretation of model output rather than a definitive measure of security.

---

## Future Improvements

Potential extensions include:

* Real-time URL feature extraction
* Larger and more diverse datasets
* Additional classification algorithms
* Hyperparameter optimization
* SHAP-based explanations
* Model versioning
* API deployment
* Authentication and rate limiting
* Real-time threat-intelligence integration
* Continuous model evaluation
* Automated model retraining

---

## Team Contributions

The project is divided into machine-learning and application components.

### Machine Learning

* Dataset inspection
* Preprocessing
* Exploratory analysis
* Feature selection
* Model training
* Model evaluation
* Explainability
* Prediction pipeline
* Risk scoring

### Application

* `app/app.py`
* `app/templates/index.html`
* `app/static/style.css`
* `app/static/script.js`
* `tests/`
* Web integration with the ML pipeline

---

## References

1. Daniel Fernando, **Web Page Phishing Dataset**, Kaggle.
   [Dataset page](https://www.kaggle.com/datasets/danielfernandon/web-page-phishing-dataset?resource=download&utm_source=chatgpt.com)
2. Aurélien Géron, *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow*.
3. Max Kuhn and Kjell Johnson, *Applied Predictive Modeling*.
4. Leo Breiman, *Random Forests*, Machine Learning, Vol. 45, No. 1.
5. Trevor Hastie, Robert Tibshirani, and Jerome Friedman, *The Elements of Statistical Learning*.

---

## Authors

**Dheeman Thakur**   - **240957082**<br>
**Sreevatsa Rajesh** - **240957021**<br>
**Arjun Sriram**     - **240957034**

Department of Computer Science
Manipal Institute of Technology, Manipal

Course: V Sem B.Tech (Mathematics & Computing) – Fundamentals of Machine Learning
The project synopsis identifies the same authors, course, institution, and project methodology.
