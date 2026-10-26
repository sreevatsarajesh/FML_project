"""Final prediction: NLP + numeric fusion with a narrow trusted-root safeguard."""

import json
from pathlib import Path
from urllib.parse import urlsplit

import joblib
import pandas as pd

from src.trusted_domains import trusted_domain
from src.url_utils import FEATURE_NAMES, canonicalize_url, extract_features

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT / "models"

nlp_model = joblib.load(MODEL_DIR / "url_nlp_model.pkl")
numeric_model = joblib.load(MODEL_DIR / "url_numeric_model.pkl")

_config = json.loads((MODEL_DIR / "fusion_config.json").read_text())
NUMERIC_WEIGHT = float(_config["numeric_weight"])
THRESHOLD = float(_config.get("threshold", 0.5))

TRUSTED_RISK_CAP = 0.05


def _positive(model, X):
    return float(model.predict_proba(X)[0][list(model.classes_).index(1)])



def _is_trusted_root(url: str) -> bool:
    try:
        value = url.strip()
        candidate = value if "://" in value else "https://" + value
        parsed = urlsplit(candidate)

        if parsed.scheme.lower() not in {"http", "https"}:
            return False

        if parsed.username or parsed.password:
            return False

        if parsed.path not in {"", "/"} or parsed.query or parsed.fragment:
            return False

        host = (parsed.hostname or "").lower().rstrip(".")
        domain = trusted_domain(url)

        return domain is not None and host == domain

    except (ValueError, TypeError, AttributeError):
        return False


def predict_fused_url(url: str, numeric_weight: float = NUMERIC_WEIGHT) -> dict:
    if not isinstance(url, str) or not url.strip():
        raise ValueError("URL must be a non-empty string.")

    if not 0.0 <= numeric_weight <= 1.0:
        raise ValueError("numeric_weight must be between 0 and 1.")

    canon = canonicalize_url(url)
    if not canon:
        raise ValueError("URL could not be parsed.")

    nlp_probability = _positive(nlp_model, [canon[:150]])
    numeric_probability = _positive(
        numeric_model,
        pd.DataFrame([extract_features(url)], columns=FEATURE_NAMES),
    )

    model_probability = (
        numeric_weight * numeric_probability
        + (1.0 - numeric_weight) * nlp_probability
    )

    domain = trusted_domain(url)
    trusted_root = _is_trusted_root(url)

    final_probability = (
        min(model_probability, TRUSTED_RISK_CAP)
        if trusted_root
        else model_probability
    )

    return {
        "numeric_probability": numeric_probability,
        "nlp_probability": nlp_probability,
        "model_probability": model_probability,
        "fused_probability": final_probability,
        "numeric_weight": numeric_weight,
        "trusted_domain": domain,
        "prediction": "phishing" if final_probability >= THRESHOLD else "benign",
    }
