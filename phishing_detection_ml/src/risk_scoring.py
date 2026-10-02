def Calc_Risk(prob):
    risk_score = prob * 100
    if risk_score >= 80:
        risk_level = "Very High"
    elif risk_score >= 60:
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
        "Risk Level": risk_level
    }