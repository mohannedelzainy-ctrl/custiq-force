# Data Dictionary & Business Metric Definitions — Custiq Force

## 1. Core Entity Identifiers
- **`customer_unique_id`**: Persistent person-level identifier used across all repeat-purchase calculations (`96,096` unique customers).
- **`customer_id`**: Order-level foreign key generated per transaction (`99,441` records). Never used alone to count unique people.
- **`order_id`**: Unique transaction identifier (`98,666` qualifying non-canceled/non-unavailable orders).

## 2. Temporal Modeling Windows
- **Observation / Feature Window**: All qualifying orders strictly prior to **`2018-03-01`** (`52,013` eligible customers).
- **Prediction / Outcome Window**: **`180 days`** forward (`2018-03-01` through `2018-08-28`).
- **`target_repeat_180d`**: Binary label (`1` if `customer_unique_id` placed >= 1 qualifying order in the 180-day window; `0` otherwise). Baseline positive rate = **`1.14%`**.

## 3. Engineered Customer Features (32 Columns)
| Feature | Formula / Description |
|---|---|
| `recency_days` | `(2018-03-01 - last_purchase) / 86400s` |
| `tenure_days` | `(2018-03-01 - first_purchase) / 86400s` |
| `frequency` | Count of distinct qualifying `order_id`s before cutoff |
| `monetary_total` | Sum of item `price` (BRL) before cutoff |
| `freight_ratio` | `freight_total / (monetary_total + 1e-5)` |
| `avg_delivery_days` | Mean actual delivery duration in days |
| `avg_delay_days` | Mean `(delivered_customer_date - estimated_delivery_date)` in days |
| `late_order_rate` | Share of historical orders delivered after estimated date |
| `avg_review_score` | Mean 1–5 star customer satisfaction rating |
