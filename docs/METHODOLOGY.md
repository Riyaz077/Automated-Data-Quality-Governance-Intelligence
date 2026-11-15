# Methodology

1. Load a CSV or generate the bundled synthetic business dataset.
2. Profile each column for type, missingness and uniqueness; summarize numeric columns.
3. Run configurable schema, null, uniqueness, numeric-range and categorical-domain rules.
4. Fit Isolation Forest to selected numeric measures and rank unusual records.
5. Compare current numeric distributions with a reference sample using PSI.
6. Produce a heuristic scorecard and downloadable issue/anomaly outputs.

PSI interpretation used in this demo: below 0.10 = Low, 0.10–0.25 = Moderate, above 0.25 = High. These are common heuristic bands, not universal acceptance criteria.
