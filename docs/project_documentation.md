# Custiq Force — Final Project Documentation (v1.0)

## Project Metadata
- **Program**: DEPI Graduation Project — Data Science
- **Supervisor**: Eng. Ahmed Mostafa
- **Submission Date**: 6 December 2026
- **Dataset**: Olist Brazilian E-Commerce Public Dataset

## Team Structure & Workstream Ownership
| Member | Role & Primary Deliverables |
|---|---|
| **Mohanned Mohammed Galal** | Project Lead; SQL queries (`src/business_metrics.sql`), business metric formulas, GitHub coordination |
| **Shahd Magdy Abdelwahd** | Dataset validation, schema profiling (`notebooks/01_data_validation_and_profiling.ipynb`), data dictionary |
| **Marwa Elbadawy Mohammed** | Data cleaning, geolocation deduplication, EDA (`notebooks/02_data_cleaning_and_eda.ipynb`) |
| **Yassin Hassan Abdelkader** | Temporal feature engineering (`src/build_ml_dataset.py`), ML modeling & evaluation (`notebooks/03_ml_modeling_and_evaluation.ipynb`) |
| **Mohammed Atef Mosa** | Interactive dashboard (`04_dashboard_handoff/app.py` & `04_dashboard_handoff/web_dashboard/index.html`), CRM segmentation & recommendations |

## Finalized Methodology & Validated Results
1. **Qualifying Orders**: Excluded `canceled` and `unavailable` statuses, yielding `98,666` qualifying orders and `R$ 15.84M` item revenue across `96,096` unique customers.
2. **Leakage-Free Temporal Cutoff (`2018-03-01`)**: Selected to leave a full `180-day` forward observation window (`2018-03-01` to `2018-08-28`) before dataset end (`2018-09`), yielding `52,013` eligible customers.
3. **Champion Model (`LogisticRegression_balanced`)**: Outperformed `RandomForest_balanced` on temporal holdout (`10,403` test customers), achieving **PR-AUC `0.0170`**, **ROC-AUC `0.5833`**, **Recall@0.60 `15.97%`**, and **Top-1% Decile Lift `3.33x`** over the `1.14%` baseline rate.
4. **Actionable Retention Tiers**:
   - **High Propensity (Top 5% — `2,601` customers, avg prob `72.1%`)**: Priority VIP retention & cross-sell offers.
   - **Medium Propensity (Next 15% — `7,802` customers, avg prob `59.0%`)**: Automated win-back emails & installment reminders.
   - **Low Propensity (Bottom 80% — `41,610` customers, avg prob `42.6%`)**: Low-cost organic lifecycle touchpoints.
