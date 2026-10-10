from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.predict import predict_url
from src.risk_scoring import Calc_Risk


app = FastAPI(
    title="Phishing Detection API",
    description="API for detecting phishing URLs using machine learning",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

class URLRequest(BaseModel):
    url: str


@app.get("/", response_class=HTMLResponse)
def HomePage():
    with open("app/templates/index.html", "r", encoding="utf-8") as file:
        return file.read()


@app.post("/predict")
def predict(data: URLRequest):
    URL = data.url
    prob = predict_url(URL)
    risk = Calc_Risk(prob)
    return risk