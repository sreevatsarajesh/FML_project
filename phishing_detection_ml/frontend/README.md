# PhishLens frontend

React + Vite UI for the FastAPI NLP + numerical URL-fusion endpoint.

## Run locally

Terminal 1 — from `phishing_detection_ml/`, activate the environment and start the API:

```bash
conda activate phishingml
uvicorn app.app:app --reload
```

Terminal 2 — start the UI:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The UI calls `http://127.0.0.1:8000` by default. To change the API address, copy `.env.example` to `.env` and set `VITE_API_URL`. Restart Vite after changing environment variables.

## API fields used

`NLP_Probability`, `Numeric_Probability`, `Model_Probability`, `Probability`, `Prediction`, `Risk Score`, `Risk Level`, `Trusted_Domain`, `Numeric_Weight`, and `Threshold`. The two model outputs and final decision are taken from the API response; the UI does not fabricate predictions.

The output is a machine-learning estimate, not a guarantee that a URL is safe or malicious.
