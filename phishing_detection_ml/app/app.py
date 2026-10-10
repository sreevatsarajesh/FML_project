from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.predict import predict_url
from src.risk_scoring import Calc_Risk

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Phishing Detection API",
    description="API for detecting phishing URLs using machine learning",
    version="1.0.0"
)


class URLRequest(BaseModel):
    url: str


@app.get("/", response_class=HTMLResponse)
def home_page():
    index_path = BASE_DIR / "templates" / "index.html"
    return HTMLResponse(
        content=index_path.read_text(encoding="utf-8")
    )


@app.post("/predict")
def predict(data: URLRequest):

    URL = data.url

    prob = predict_url(URL)

    risk = Calc_Risk(prob)

    return risk