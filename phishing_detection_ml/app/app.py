
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

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
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
    url = data.url.strip()

    if not url:
        raise HTTPException(
            status_code=400,
            detail="Please enter a URL."
        )

    try:
        probability = predict_url(url)
        risk = Calc_Risk(probability)

        if not isinstance(risk, dict):
            raise ValueError("Calc_Risk must return a dictionary.")

        return {
            **risk,
            "Probability": probability
        }

    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
