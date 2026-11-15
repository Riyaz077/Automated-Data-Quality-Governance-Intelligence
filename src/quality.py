import numpy as np
import pandas as pd

RULES = {
    "required_columns": ["record_id","customer_id","region","order_value","quantity","days_to_ship","order_status"],
    "numeric_ranges": {"order_value": (0, 100000), "quantity": (1, 1000),
                       "days_to_ship": (0, 30), "customer_satisfaction": (1, 5)},
    "allowed_values": {"region": ["North","South","East","West"],
                       "order_status": ["Delivered","Pending","Cancelled","Returned"]}
}

def profile_dataset(df):
    n = len(df)
    rows = []
    for col in df.columns:
        s = df[col]
        rows.append({
            "column": col, "dtype": str(s.dtype),
            "missing_count": int(s.isna().sum()),
            "missing_pct": float(s.isna().mean()*100) if n else 0.0,
            "unique_count": int(s.nunique(dropna=True)),
            "unique_pct": float(s.nunique(dropna=True)/n*100) if n else 0.0
        })
    numeric = df.select_dtypes(include="number").describe().T.reset_index().rename(columns={"index":"column"})
    return pd.DataFrame(rows), numeric

def validate_dataset(df, rules=None):
    rules = rules or RULES
    issues = []
    for col in rules["required_columns"]:
        if col not in df.columns:
            issues.append({"rule":"required_column_exists","column":col,"issue_count":len(df),
                           "severity":"Critical","details":"Required column is missing"})
        else:
            count = int(df[col].isna().sum())
            if count:
                issues.append({"rule":"not_null","column":col,"issue_count":count,
                               "severity":"High","details":"Required values are missing"})
    if "record_id" in df.columns:
        count = int(df["record_id"].duplicated(keep=False).sum())
        if count:
            issues.append({"rule":"unique_key","column":"record_id","issue_count":count,
                           "severity":"High","details":"Duplicate record identifiers"})
    for col, (low, high) in rules["numeric_ranges"].items():
        if col in df.columns:
            values = pd.to_numeric(df[col], errors="coerce")
            count = int(((values < low) | (values > high) | values.isna()).sum())
            if count:
                issues.append({"rule":"numeric_range","column":col,"issue_count":count,
                               "severity":"Medium","details":f"Expected values between {low} and {high}"})
    for col, allowed in rules["allowed_values"].items():
        if col in df.columns:
            count = int((~df[col].isin(allowed) & df[col].notna()).sum())
            if count:
                issues.append({"rule":"allowed_values","column":col,"issue_count":count,
                               "severity":"Medium","details":"Values outside configured domain"})
    return pd.DataFrame(issues, columns=["rule","column","issue_count","severity","details"])

def quality_score(df, issues):
    if len(df) == 0:
        return 0.0
    total = len(df)
    penalty = 0.0
    if not issues.empty:
        weights = {"Critical": 3.0, "High": 2.0, "Medium": 1.0, "Low": .5}
        penalty = sum(min(1.0, row.issue_count/total) * weights.get(row.severity,1)
                      for row in issues.itertuples())
    return round(max(0.0, 100.0 - 100.0*penalty/10.0), 2)
