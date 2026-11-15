from src.data import generate_business_data, generate_reference_data
from src.quality import profile_dataset, validate_dataset, quality_score
from src.anomaly import detect_anomalies
from src.drift import compare_numeric_drift

def test_profile_and_rules():
    df=generate_business_data(300,seed=4)
    profile,summary=profile_dataset(df)
    issues=validate_dataset(df)
    assert len(profile)==len(df.columns)
    assert not issues.empty
    assert 0 <= quality_score(df,issues) <= 100

def test_anomaly_flags():
    df=generate_business_data(250,seed=8)
    out=detect_anomalies(df)
    assert "anomaly_flag" in out
    assert out.anomaly_flag.any()

def test_drift_comparison():
    ref=generate_reference_data(300,seed=1)
    cur=generate_business_data(300,seed=2,corrupt=False)
    result=compare_numeric_drift(ref,cur)
    assert "psi" in result.columns
