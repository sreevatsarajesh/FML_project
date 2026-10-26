import sys
from pathlib import Path
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.fusion_v2 import predict_fused_url, THRESHOLD

INPUT = ROOT / "data" / "evaluation_urls.csv"
OUTPUT = ROOT / "results" / "evaluation_urls_predictions.csv"


def calculate_metrics(y_true, y_pred):
    tn, fp, fn, tp = confusion_matrix(
        y_true, y_pred, labels=[0, 1]
    ).ravel()
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(
            y_true, y_pred, zero_division=0
        ),
        "recall": recall_score(
            y_true, y_pred, zero_division=0
        ),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "false_positive_rate": (
            fp / (fp + tn) if (fp + tn) else 0.0
        ),
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp,
    }


def main():
    data = pd.read_csv(INPUT)
    required = {"url", "label", "category"}
    if not required.issubset(data.columns):
        raise ValueError(f"CSV must contain columns: {required}")
    if data.empty:
        raise ValueError("Evaluation CSV is empty.")
    if data["label"].isna().any() or not data["label"].isin([0, 1]).all():
        raise ValueError("Labels must be 0 (legitimate) or 1 (phishing).")
    records = []
    for row in data.itertuples(index=False):
        result = predict_fused_url(row.url)
        records.append({
            "url": row.url,
            "label": int(row.label),
            "category": row.category,
            "numeric_probability": result["numeric_probability"],
            "nlp_probability": result["nlp_probability"],
            "model_probability": result["model_probability"],
            "fused_probability": result["fused_probability"],
            "trusted_domain": result["trusted_domain"],
            "raw_prediction": int(
                result["model_probability"] >= THRESHOLD
            ),
            "final_prediction": int(
                result["prediction"] == "phishing"
            ),
        })
    results = pd.DataFrame(records)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT, index=False)
    y_true = results["label"]
    for name, column in [
        ("Raw model (no trusted-root cap)", "raw_prediction"),
        ("Final system (with trusted-root cap)", "final_prediction"),
    ]:
        print(f"\n{name}")
        for metric, value in calculate_metrics(
            y_true, results[column]
        ).items():
            print(f"  {metric}: {value:.4f}" if isinstance(value, float)
                  else f"  {metric}: {value}")
    print(f"\nPer-URL results saved to: {OUTPUT}")

if __name__ == "__main__":
    main()
