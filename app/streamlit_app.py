from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import streamlit as st
import pandas as pd
import plotly.express as px
from src.data import generate_business_data, generate_reference_data
from src.engine import run_assessment

st.set_page_config(page_title="DataTrust",page_icon="🧭",layout="wide")
st.title("🧭 DataTrust")
st.caption("Automated Data Quality, Anomaly Detection and Business Data Governance")
uploaded=st.sidebar.file_uploader("Upload business CSV",type=["csv"])
if uploaded:
    df=pd.read_csv(uploaded)
else:
    path=Path(__file__).resolve().parents[1]/"data"/"business_data.csv"
    df=pd.read_csv(path) if path.exists() else generate_business_data()
ref_path=Path(__file__).resolve().parents[1]/"data"/"reference_data.csv"
reference=pd.read_csv(ref_path) if ref_path.exists() else generate_reference_data()
with st.spinner("Profiling data, validating rules and detecting anomalies..."):
    result=run_assessment(df,reference)
a,b,c,d=st.columns(4)
a.metric("Quality score",f"{result['quality_score']:.1f}/100")
b.metric("Records",f"{len(df):,}")
c.metric("Rule issue types",len(result["issues"]))
d.metric("Anomalies flagged",int(result["anomalies"]["anomaly_flag"].sum()))
tab1,tab2,tab3,tab4=st.tabs(["Overview","Quality Rules","Anomalies","Drift"])
with tab1:
    st.subheader("Column-level data profile")
    st.dataframe(result["profile"],use_container_width=True)
    if not result["numeric_summary"].empty:
        st.subheader("Numeric summary")
        st.dataframe(result["numeric_summary"],use_container_width=True)
with tab2:
    st.subheader("Validation findings")
    if result["issues"].empty: st.success("No configured rule violations found.")
    else:
        st.dataframe(result["issues"],use_container_width=True)
        st.plotly_chart(px.bar(result["issues"],x="column",y="issue_count",color="severity",
                               title="Issue counts by column"),use_container_width=True)
with tab3:
    st.subheader("Isolation Forest anomaly review")
    st.dataframe(result["anomalies"].head(100),use_container_width=True)
    st.download_button("Download anomaly report",
        result["anomalies"].to_csv(index=False).encode("utf-8"),"datatrust_anomalies.csv","text/csv")
with tab4:
    st.subheader("Reference vs current numeric drift")
    if result["drift"].empty: st.info("No comparable numeric columns available.")
    else: st.dataframe(result["drift"],use_container_width=True)
st.download_button("Download quality issues",
    result["issues"].to_csv(index=False).encode("utf-8"),"datatrust_quality_issues.csv","text/csv")
st.info("Anomaly flags and quality scores are review aids. Validate rules with business data owners.")
