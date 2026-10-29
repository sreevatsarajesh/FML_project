# Phishing Detection ML

**A machine learning-powered phishing URL detection system combining numerical URL analysis, NLP, and an interactive security dashboard.**

Phishing Detection ML analyzes URLs and estimates whether they exhibit characteristics associated with phishing attacks. It combines URL structure analysis with text-based pattern recognition to produce a prediction and risk score through a FastAPI backend.

The project aims to make preliminary URL security analysis accessible through a simple, interactive web interface.

## Features

- **URL Classification:** Analyze submitted URLs for potential phishing activity.
- **Numeric URL Analysis:** Examine structural characteristics and patterns in URLs.
- **NLP-Based Analysis:** Use text-based features to identify potentially suspicious URL patterns.
- **Model Fusion:** Combine model outputs to support the final prediction.
- **Risk Scoring:** Convert the resulting probability into a score from 0 to 100.
- **Trusted-Domain Matching:** Check URLs against a configurable set of recognized domains.
- **Interactive Dashboard:** Display predictions, risk scores, model probabilities, and recent evaluations.
- **REST API:** Expose prediction functionality through FastAPI.
- **API Documentation:** Explore and test endpoints using the automatically generated Swagger UI.

## How It Works

```text
                  User submits a URL
                          |
                          v
                  FastAPI Backend
                          |
                          v
                  URL Processing
                          |
              +-----------+-----------+
              |                       |
              v                       v
       Numeric Analysis          NLP Analysis
              |                       |
              +-----------+-----------+
                          |
                          v
                   Model Fusion
                          |
                          v
                  Final Probability
                          |
                 +--------+--------+
                 |                 |
                 v                 v
           Classification      Risk Scoring
                 |                 |
                 +--------+--------+
                          |
                          v
                 Dashboard Results
```

### 1. URL Processing

The submitted URL is processed before being passed to the prediction pipeline. URL normalization and feature extraction help prepare the input for analysis.

### 2. Numeric URL Analysis

The numeric component analyzes measurable URL characteristics. Depending on the implemented feature set, these may include URL length, domain structure, special-character patterns, and other structural indicators.

### 3. NLP Analysis

The NLP component examines textual patterns in URLs. Character-level text features can help identify suspicious sequences that may not be obvious from individual words alone.

### 4. Model Fusion

The fusion component combines information from the numeric and NLP models to calculate the final prediction probability.

The effectiveness of fusion depends on the models, their training data, and the fusion strategy. It should be evaluated against individual model baselines.

### 5. Classification and Risk Scoring

The final probability is converted into a risk score:

`Risk Score = Probability × 100`

The probability is also compared against a configurable classification threshold. The threshold determines the classification decision, while risk-level labels are assigned separately according to the application's configured score bands.

### 6. Results Dashboard

The frontend presents the classification, risk score, model outputs, and trusted-domain information to help users understand the result.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend and machine learning |
| FastAPI | REST API |
| Scikit-learn | Machine learning and text-feature pipelines |
| TF-IDF | Text feature representation, where used by the NLP pipeline |
| HTML and CSS | User interface and styling |
| JavaScript | API requests and dynamic dashboard updates |
| Uvicorn | ASGI application server |

## Getting Started

### Prerequisites

- Python 3.10 or a compatible version for the installed dependencies
- pip
- Git
- A modern web browser

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd phishing_detection_ml
```

Replace the placeholder with the actual repository URL.

### 2. Create and activate the environment

If you use Conda:

```bash
conda create -n phishingml python=3.10
conda activate phishingml
```

Alternatively, create a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If the repository includes a `requirements.txt` file:

```bash
python -m pip install -r requirements.txt
```

Otherwise, install the dependencies listed by your project's existing environment and dependency files.

### 4. Check the model files

Ensure the trained model artifacts expected by the prediction code are present in the appropriate `models/` directory.

Depending on the current implementation, these may include the numeric model, the NLP classifier, and any fitted text-processing objects.

The application cannot produce valid predictions if required model artifacts are missing or incompatible.

### 5. Start the backend

From the repository root, if the FastAPI application is located at `app/app.py`:

```bash
uvicorn app.app:app --reload
```

The application should be available at:

- **Web dashboard:** http://127.0.0.1:8000/
- **Swagger API documentation:** http://127.0.0.1:8000/docs
- **ReDoc documentation:** http://127.0.0.1:8000/redoc

If your entry point differs, adjust the Uvicorn module path to match your project structure.

## API Usage

### `POST /predict`

Submit a URL for analysis.

**Request body:**

```json
{
  "url": "https://example.com"
}
```

**Example using cURL:**

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

The response fields depend on the active prediction implementation. They may include:

| Field | Description |
|---|---|
| `Prediction` | Final classification label |
| `Probability` | Final prediction probability |
| `Risk Score` | Probability scaled to 0–100 |
| `Risk Level` | Application-defined risk category |
| `Numeric_Probability` | Numeric model output, if exposed |
| `NLP_Probability` | NLP model output, if exposed |
| `Threshold` | Classification threshold |
| `Trusted_Domain` | Recognized trusted domain, if matched |

The exact JSON schema should be verified against the currently running API.

## Testing

Test the application with a range of known legitimate URLs and appropriately labeled phishing samples from reputable datasets.

### Legitimate baseline examples

- `https://www.google.com/`
- `https://github.com/`
- `https://www.gov.uk/`
- `https://www.canada.ca/`
- `https://www.india.gov.in/`

These are useful for evaluating whether legitimate domains are incorrectly flagged. They are examples for testing, not a guarantee that the current model will classify every URL correctly.

### Suspicious-looking test inputs

Use reserved example domains to test suspicious-looking URL patterns without targeting real organizations.

- `http://paypal-login.example.com`
- `https://account-verify.example.org`
- `https://secure-update.example.net`

These are synthetic test inputs, not real phishing websites.

### Evaluation metrics

For a meaningful evaluation, measure:

- **Accuracy:** Overall proportion of correct predictions.
- **Precision:** How often phishing predictions are correct.
- **Recall:** How many actual phishing samples are detected.
- **F1-score:** The harmonic mean of precision and recall.
- **Confusion matrix:** Counts true positives, true negatives, false positives, and false negatives.

Evaluate on held-out data and avoid reporting metrics calculated on training data as evidence of generalization.

## Limitations

- A model prediction is an estimate, not proof that a website is malicious or safe.
- Legitimate websites may be incorrectly classified as phishing.
- Newly created phishing URLs may not resemble the model's training data.
- Trusted-domain lists can be incomplete or outdated.
- Domain names and URL structure alone cannot establish the safety of a website.
- A risk score is not necessarily a calibrated real-world probability of harm.

## Future Improvements

- Improve false-positive and false-negative analysis.
- Expand and maintain verified trusted-domain coverage.
- Calibrate model probabilities and evaluate different classification thresholds.
- Compare numeric, NLP, and fused models using consistent evaluation datasets.
- Add explainability to show which features contributed to a prediction.
- Test against unseen domains and periodically updated phishing datasets.
- Improve API validation, error handling, and automated regression testing.

## Security Notice

This project is intended for educational, research, and defensive cybersecurity purposes. It provides preliminary URL analysis and should not be treated as a replacement for browser security protections, threat intelligence, or professional security assessment.

Do not enter real passwords, banking details, or other sensitive information into suspicious websites while testing.

## Contributing

Contributions, bug reports, model evaluations, and suggestions for improving detection reliability are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request describing the change and its evaluation.

**Built as a machine learning and defensive cybersecurity project.**