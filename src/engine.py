import pandas as pd
from src.quality import profile_dataset, validate_dataset, quality_score
from src.anomaly import detect_anomalies
from src.drift import compare_numeric_drift

def run_assessment(df, reference_df=None):
    profile, numeric = profile_dataset(df)
    issues = validate_dataset(df)
    scored = detect_anomalies(df)
    drift = compare_numeric_drift(reference_df,df) if reference_df is not None else pd.DataFrame()
    return {
        "profile":profile, "numeric_summary":numeric, "issues":issues,
        "anomalies":scored, "drift":drift, "quality_score":quality_score(df,issues)
    }
