from flask import Flask, request
from src.predict import predict_url
app = Flask('Phishing_Detection')

@app.route("/")
def HomePage():
    return "<p>Hi!!</p>"

@app.route("/predict", methods=['POST'])
def predict():
        data = request.get_json()
        URL = data["url"]
        prob = predict_url(URL)
        return{
              "Probability" : prob
        }

