
from pathlib import Path

import joblib
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

FEATURES = [
    "n_slash",
    "n_hypens",
    "n_redirection",
    "count",
    "n_equal",
    "url_length",
    "n_and",
    "n_dots",
    "n_questionmark",
    "n_at",
    "n_plus",
    "n_space",
    "n_percent",
    "n_dollar",
    "n_asterisk",
]

models = {
    "logistic_regression": joblib.load(
        MODEL_DIR / "logistic_regression_optimized.pkl"
    ),
    "decision_tree": joblib.load(
        MODEL_DIR / "decision_tree_optimized.pkl"
    ),
    "random_forest": joblib.load(
        MODEL_DIR / "random_forest_optimized.pkl"
    ),
}


def extract_features(url: str) -> pd.DataFrame:
    """Extract the model's URL features.

    n_redirection is an approximation: count occurrences of
    common redirect indicators. count=1 is a provisional
    convention because the dataset's count is group metadata.
    """
    url = url.strip()

    features = {
        "n_slash": url.count("/"),
        "n_hypens": url.count("-"),
        "n_redirection": url.count("://") - 1,
        "count": 1,
        "n_equal": url.count("="),
        "url_length": len(url),
        "n_and": url.count("&"),
        "n_dots": url.count("."),
        "n_questionmark": url.count("?"),
        "n_at": url.count("@"),
        "n_plus": url.count("+"),
        "n_space": url.count(" "),
        "n_percent": url.count("%"),
        "n_dollar": url.count("$"),
        "n_asterisk": url.count("*"),
    }

    return pd.DataFrame([features], columns=FEATURES)


def predict_url(
    url: str,
    model_name: str = "random_forest",
) -> float:
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string.")

    if model_name not in models:
        raise ValueError(
            f"Unknown model '{model_name}'. Choose from: "
            f"{', '.join(models)}"
        )

    features = extract_features(url)
    model = models[model_name]

    probabilities = model.predict_proba(features)
    classes = list(model.classes_)
    phishing_index = classes.index(1)

    return float(probabilities[0][phishing_index])
