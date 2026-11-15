# DataTrust
## Automated Data Quality, Anomaly Detection and Business Data Governance Platform

DataTrust is an end-to-end data observability and governance portfolio project. It profiles business datasets, evaluates configurable quality rules, detects unusual records, compares current data with a reference baseline, and produces a governance-oriented quality scorecard.

### Core capabilities
- Automated dataset profiling: completeness, uniqueness, validity, numeric summaries and categorical distributions.
- Configurable quality rules for required fields, duplicates, numeric ranges and allowed categories.
- Row-level anomaly detection using Isolation Forest.
- Reference-vs-current distribution monitoring using Population Stability Index (PSI).
- Business-facing data quality score, issue summary and downloadable reports.
- Streamlit dashboard and FastAPI endpoints.
- Synthetic business dataset, notebook, documentation and tests.

### Quick start
Python 3.10+ recommended.

```bash
pip install -r requirements.txt
python scripts/generate_data.py
streamlit run app/streamlit_app.py
```

Run the API in another terminal:
```bash
uvicorn api.main:app --reload
```

### Use your own data
Upload a CSV in the dashboard. The demo rule configuration expects:
- `record_id` — unique record key
- `customer_id` — customer identifier
- `region` — category
- `order_value` — non-negative numeric amount
- `quantity` — positive integer-like value
- `days_to_ship` — non-negative numeric measure
- `order_status` — one of `Delivered`, `Pending`, `Cancelled`, `Returned`

The profiling and anomaly functions can also be adapted to other schemas.

### Project structure
```text
DataTrust/
├── api/              # FastAPI endpoints
├── app/              # Streamlit dashboard
├── data/             # Synthetic sample and reference datasets
├── docs/             # Methodology, rules and governance notes
├── notebooks/        # Exploratory walkthrough
├── scripts/          # Synthetic data generator
├── src/              # Profiling, validation, anomaly and drift logic
├── tests/            # Unit tests
├── requirements.txt
└── README.md
```

### Important limitations
This is an educational portfolio prototype, not a certified governance or regulatory-compliance product. The included data is synthetic. Quality rules are illustrative and should be adapted with data owners and domain experts. Anomaly flags are statistical review signals, not proof of errors or misconduct. PSI thresholds are heuristic. Do not use the score as a substitute for legal, privacy, security or regulatory assessment.
