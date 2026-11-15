from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from fastapi import FastAPI, HTTPException
import pandas as pd
from src.data import generate_business_data, generate_reference_data
from src.engine import run_assessment

app=FastAPI(title="DataTrust API",version="1.0.0",
 description="Educational data quality, anomaly detection and drift assessment API.")

@app.get("/health")
def health():
    return {"status":"ok","project":"DataTrust"}

@app.get("/assess/demo")
def assess_demo():
    try:
        result=run_assessment(generate_business_data(1200,seed=12),
                              generate_reference_data(1200,seed=21))
        return {
            "quality_score":result["quality_score"],
            "profile":result["profile"].to_dict(orient="records"),
            "issues":result["issues"].to_dict(orient="records"),
            "anomaly_count":int(result["anomalies"]["anomaly_flag"].sum()),
            "drift":result["drift"].to_dict(orient="records")
        }
    except Exception as exc:
        raise HTTPException(status_code=500,detail=str(exc))

@app.post("/assess/csv")
async def assess_csv():
    raise HTTPException(status_code=501,
        detail="CSV upload endpoint is not enabled in this demo. Use the Streamlit dashboard or Python engine.")
