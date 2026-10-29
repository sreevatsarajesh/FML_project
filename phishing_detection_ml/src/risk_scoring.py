
import math

def Calc_Risk(prob, threshold=0.3):
    if not isinstance(prob, (int, float)) or isinstance(prob, bool):
        raise ValueError("Probability must be a numeric value.")

    if not math.isfinite(prob) or not 0.0 <= prob <= 1.0:
        raise ValueError("Probability must be between 0 and 1.")

    if not isinstance(threshold, (int, float)) or isinstance(threshold, bool):
        raise ValueError("Threshold must be a numeric value.")

    if not math.isfinite(threshold) or not 0.0 <= threshold <= 1.0:
        raise ValueError("Threshold must be between 0 and 1.")

    risk_score = prob * 100

    if risk_score >= 70:
        risk_level = "High"
    elif risk_score >= 40:
        risk_level = "Medium"
    elif risk_score >= 20:
        risk_level = "Low"
    else:
        risk_level = "Very Low"

    return {
        "Probability": prob,
        "Risk Score": risk_score,
        "Risk Level": risk_level,
    }
