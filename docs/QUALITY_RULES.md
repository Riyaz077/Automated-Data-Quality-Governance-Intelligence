# Configured Quality Rules

| Rule | Default behaviour | Severity |
|---|---|---|
| Required column exists | Checks key business fields are present | Critical |
| Not null | Counts missing values in required fields | High |
| Unique key | Detects duplicate `record_id` values | High |
| Numeric range | Checks amount, quantity, shipping time and satisfaction bounds | Medium |
| Allowed values | Checks region and order-status domains | Medium |

Edit `RULES` in `src/quality.py` to adapt checks to a different dataset. Confirm business definitions and thresholds with data owners before using results operationally.
