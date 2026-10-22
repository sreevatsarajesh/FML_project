def Calc_Risk(prob, threshold=0.3):
    risk_score = prob * 100

    if prob >= threshold:
        risk_level = "High"
    elif risk_score >= 20:
        risk_level = "Medium"
    elif risk_score >= 10:
        risk_level = "Low"
    else:
        risk_level = "Very Low"

    return {
        "Probability": prob,
        "Risk Score": risk_score,
        "Risk Level": risk_level
    }
