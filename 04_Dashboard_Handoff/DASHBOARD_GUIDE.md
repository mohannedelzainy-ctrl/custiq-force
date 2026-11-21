# Dashboard guide — Custiq Force

## Suggested dashboard pages

### 1. Executive overview
- Eligible historical customers
- Repeat-purchase rate in the defined 180-day label window
- Average historical spend and average order value
- Customers by propensity segment
- Clear note: historical Olist snapshot, not live customer data

### 2. Customer segments
- Bar chart: customer count by `propensity_segment`
- Bar chart: average `predicted_repeat_probability` by segment
- Filters: `customer_state`, `customer_city`, and propensity segment
- Table: customer ID, location, probability, percentile, segment

### 3. Model quality
- Show Average Precision (PR-AUC), ROC-AUC, and positive-class baseline from `model_metrics.csv`
- Show top-k lift from `top_k_lift_metrics.csv`
- State that evaluation uses a stratified random holdout from one historical snapshot
- Explain the low target prevalence; do not use accuracy as the main quality metric

### 4. Campaign experiment tracking (future data required)
- Treatment vs control group
- Offer cost and discount amount
- Incremental conversion, revenue, margin, and redemption
- This page cannot be populated correctly from the Olist historical dataset alone; campaign assignment and outcome data must be collected first.

## Files to load

- `output/customer_propensity_scores.csv`
- `output/model_metrics.csv`
- `output/top_k_lift_metrics.csv`

## Important interpretation

`predicted_repeat_probability` estimates repeat-purchase propensity, not the incremental effect of an offer. A high-propensity customer may return without a discount. Do not label the segment as "send offer" unless a controlled experiment or uplift model supports that decision.
