import numpy as np
import pandas as pd

def generate_business_data(n=4000, seed=42, corrupt=True):
    rng = np.random.default_rng(seed)
    regions = np.array(["North", "South", "East", "West"])
    statuses = np.array(["Delivered", "Pending", "Cancelled", "Returned"])
    df = pd.DataFrame({
        "record_id": [f"ORD{i:07d}" for i in range(n)],
        "customer_id": [f"CUST{x:05d}" for x in rng.integers(1, 1200, n)],
        "region": rng.choice(regions, n, p=[.26,.30,.20,.24]),
        "order_value": np.round(rng.gamma(3.2, 420, n), 2),
        "quantity": rng.integers(1, 12, n),
        "days_to_ship": np.maximum(0, rng.normal(3.8, 1.7, n)).round(1),
        "order_status": rng.choice(statuses, n, p=[.72,.12,.10,.06]),
        "customer_satisfaction": np.clip(rng.normal(4.0, .7, n), 1, 5).round(1)
    })
    if corrupt and n >= 50:
        # Controlled, synthetic data-quality defects for demonstration.
        missing_idx = rng.choice(n, max(1, n//100), replace=False)
        df.loc[missing_idx, "region"] = None
        bad_idx = rng.choice(n, max(1, n//200), replace=False)
        df.loc[bad_idx, "order_value"] = -abs(df.loc[bad_idx, "order_value"])
        dup_idx = rng.choice(n, max(1, n//250), replace=False)
        df.loc[dup_idx, "record_id"] = df.loc[dup_idx, "record_id"].iloc[0]
        out_idx = rng.choice(n, max(1, n//300), replace=False)
        df.loc[out_idx, "days_to_ship"] = rng.uniform(25, 60, len(out_idx)).round(1)
    return df

def generate_reference_data(n=4000, seed=21):
    return generate_business_data(n=n, seed=seed, corrupt=False)
