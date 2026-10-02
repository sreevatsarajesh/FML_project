from flask import Flask, request, render_template
from src.predict import predict_url
from src.risk_scoring import Calc_Risk
app = Flask('Phishing_Detection')

@app.route("/")
def HomePage():
    return render_template("index.html")

@app.route("/predict", methods=['POST'])
def predict():
        data = request.get_json()
        URL = data["url"]
        prob = predict_url(URL)
        risk = Calc_Risk(prob)
        return risk
        



