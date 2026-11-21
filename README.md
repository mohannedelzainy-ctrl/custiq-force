# Custiq Force — Olist E-Commerce Analytics & Repeat-Purchase Prediction

This repository is organized sequentially across the **4 core project functions** so each team member can run their module independently with zero path conflicts or data leakage:

1. **`01_Data_Collection/`** *(Completed)*
   - `raw_data/`: Original 9 Olist CSV datasets.
   - `01_data_collection_profiling.ipynb`: Automated schema, primary/foreign key, and initial quality profiling.
   - `profiling_reports/`: Exported CSV profiling summaries.

2. **`02_Data_Cleaning_and_EDA/`** *(Completed)*
   - `02a_data_cleaning.ipynb`: Data type parsing, referential integrity checks, outlier inspection, missing category imputation, and export to `cleaned_data/`.
   - `02b_exploratory_analysis.ipynb`: 13 publication-ready visualizations saved in `figures/` plus quantified business insights.
   - `cleaned_data/`: All 9 cleaned CSV tables.

3. **`03_Machine_Learning/`** *(Completed)*
   - `build_ml_dataset.py`: Leakage-free temporal snapshot generator (`2018-03-01` cutoff, `180-day` future window) producing `ml_data/ml_customer_dataset.csv` (`52,013` customers × `32` columns).
   - `03_ml_modeling.ipynb`: Validation-only model and threshold selection (`LogisticRegression_balanced` achieving `3.33x` lift in Top 1%), untouched hold-out test evaluation, and full-snapshot propensity scoring.
   - `model_artifacts/`: Serialized model (`repeat_purchase_model.joblib`), evaluation metrics, diagnostic curves, and `customer_propensity_scores.csv`.

4. **`04_Dashboard_Handoff/`** *(Ready for Dashboard Designer)*
   - `DASHBOARD_GUIDE.md`: Page-by-page specification (Executive Overview, Customer Segments, Model Quality, and Campaign Experiment Tracking).
   - `04_dashboard_starter.ipynb`: Verification notebook confirming exact KPI numbers and table schemas.
   - `dashboard_ready_data/`: All pre-cleaned and ML-scored CSV files ready for Power BI, Tableau, or Streamlit.
