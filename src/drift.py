import numpy as np
import pandas as pd

def population_stability_index(reference, current, bins=10):
    ref = pd.to_numeric(pd.Series(reference), errors="coerce").dropna().to_numpy()
    cur = pd.to_numeric(pd.Series(current), errors="coerce").dropna().to_numpy()
    if len(ref) == 0 or len(cur) == 0:
        return float("nan")
    edges = np.unique(np.quantile(ref, np.linspace(0,1,bins+1)))
    if len(edges) < 3:
        edges = np.linspace(ref.min()-1e-9, ref.max()+1e-9, bins+1)
    edges[0] = -np.inf
    edges[-1] = np.inf
    r = np.histogram(ref, bins=edges)[0] / len(ref)
    c = np.histogram(cur, bins=edges)[0] / len(cur)
    eps = 1e-6
    r = np.clip(r,eps,None); c = np.clip(c,eps,None)
    return float(np.sum((c-r)*np.log(c/r)))

def compare_numeric_drift(reference_df, current_df, columns=None):
    columns = columns or sorted(set(reference_df.select_dtypes("number").columns) &
                                set(current_df.select_dtypes("number").columns))
    rows=[]
    for col in columns:
        if col in reference_df and col in current_df:
            psi=population_stability_index(reference_df[col],current_df[col])
            label="Low" if psi < .1 else "Moderate" if psi < .25 else "High"
            rows.append({"column":col,"psi":psi,"drift_level":label})
    return pd.DataFrame(rows)
