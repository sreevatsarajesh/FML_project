def predict_url(url):
    """
    Mock phishing prediction.
    Parameters:
        url (str): URL to evaluate.
    Returns:
        float: Mock phishing probability between 0 and 1.
    """
    if "login" in url.lower():
        probability = 0.80
    else:
        probability = 0.20
    return probability