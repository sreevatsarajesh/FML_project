from pathlib import Path
from src.fusion_v2 import NUMERIC_WEIGHT, THRESHOLD, predict_fused_url
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from src.fusion_v2 import NUMERIC_WEIGHT, predict_fused_url
from src.risk_scoring import Calc_Risk

BASE_DIR = Path(__file__).resolve().parent
MAX_URL_LENGTH = 2048

app = FastAPI(
    title="Phishing Detection API",
    description="Detects phishing URLs using numeric + NLP model fusion "
                "with a trusted-domain safety net",
    version="1.2.0",
)

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


class URLRequest(BaseModel):
    url: str


@app.get("/", response_class=HTMLResponse)
def home_page():
    index_path = BASE_DIR / "templates" / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=500, detail="Homepage template was not found.")
    return HTMLResponse(content=index_path.read_text(encoding="utf-8"))


@app.get("/health")
def health():
    return {"status": "ok", "model": "fusion", "numeric_weight": NUMERIC_WEIGHT}


@app.post("/predict")
def predict(data: URLRequest):
    url = data.url.strip()

    if not url:
        raise HTTPException(status_code=400, detail="Please enter a URL.")
    if len(url) > MAX_URL_LENGTH:
        raise HTTPException(status_code=400, detail="URL is too long.")

    try:
        result = predict_fused_url(url)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check model files and server logs.",
        )

    probability = result["fused_probability"]
    risk = Calc_Risk(probability, threshold=THRESHOLD)

    return {
        **risk,
        "Probability": probability,
        "Prediction": result["prediction"],
        "Numeric_Probability": result["numeric_probability"],
        "NLP_Probability": result["nlp_probability"],
        "Model_Probability": result["model_probability"],
        "Trusted_Domain": result["trusted_domain"],
        "Model": "Fusion",
        "Numeric_Weight": result["numeric_weight"],
    }
