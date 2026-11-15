import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

DEFAULT_FEATURES = ["order_value","quantity","days_to_ship"]

def detect_anomalies(df, contamination=0.04, features=None, random_state=42):
    features = features or [c for c in DEFAULT_FEATURES if c in df.columns]
    if len(features) < 1:
        raise ValueError("At least one numeric feature is required.")
    X = df[features].apply(pd.to_numeric, errors="coerce")
    X = X.replace([np.inf,-np.inf], np.nan)
    medians = X.median().fillna(0)
    X = X.fillna(medians)
    model = IsolationForest(contamination=contamination, random_state=random_state)
    labels = model.fit_predict(X)
    scores = -model.score_samples(X)
    out = df.copy()
    out["anomaly_flag"] = (labels == -1)
    out["anomaly_score"] = scores
    return out.sort_values("anomaly_score", ascending=False).reset_index(drop=True)
