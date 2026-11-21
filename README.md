# Custiq Force — E-Commerce Customer Intelligence & Retention
**DEPI Graduation Project — Data Science**

| Field | Details |
|---|---|
| **Program** | DEPI Graduation Project — Data Science |
| **Supervisor** | Eng. Ahmed Mostafa |
| **Submission Date** | 6 December 2026 |
| **Dataset** | Olist Brazilian E-Commerce Public Dataset |
| **GitHub Repository** | `https://github.com/mohannedelzainy-ctrl/custiq-force` |
| **Document Status** | **Final v1.0 — Analysis, Modeling & Dashboard Completed** |

---

## 1. Executive Summary
**Custiq Force** is an end-to-end Data Science and Machine Learning solution built on the **Olist Brazilian E-Commerce Public Dataset** (`96,096` unique customers, `98,666` qualifying orders, and `R$ 15.84M` in item revenue). The project solves a core e-commerce retention problem: **identifying the rare `~1.14%` of customers likely to place a repeat purchase within 180 days**, enabling marketing teams to focus retention spend on high-propensity cohorts rather than untargeted mass discounts.

Using a strict point-in-time feature store at cutoff **`2018-03-01`** (`52,013` eligible customers × `32` behavioral, RFM, payment, review, and delivery SLA features), our calibrated **`LogisticRegression_balanced`** model achieved a **3.33x Top-1% Decile Targeting Lift** on temporal holdout evaluation (`10,403` test customers) and stratified all active customers into three actionable CRM retention tiers.

---

## 2. Project Information
- **Program:** DEPI Graduation Project — Data Science
- **Supervisor:** Eng. Ahmed Mostafa
- **Submission Date:** 6 December 2026
- **Dataset:** Olist Brazilian E-Commerce Public Dataset
- **Document Status:** Final v1.0 — Completed & Validated

---

## 3. Background and Business Problem
E-commerce marketplaces often struggle with low repeat-purchase conversion (`~1.14%` within 180 days in the Olist cohort) and high customer acquisition costs. Without predictive segmentation, retention campaigns either waste budget on mass discounts or fail to reach high-value customers before they churn.

Custiq Force provides a reproducible, leakage-free analytical pipeline that connects raw multi-table order logs with SQL business metrics, interpretable machine learning propensity scores, and an interactive decision-support dashboard.

---

## 4. Project Objectives
1. **Repeat-Purchase Propensity Prediction:** Estimate each customer's probability of placing a repeat qualifying order within a `180-day` forward window (`2018-03-01` to `2018-08-28`).
2. **At-Risk & Retention Tier Segmentation:** Classify customers into three operational retention cohorts (`High — Top 5%`, `Medium — Next 15%`, and `Low — Bottom 80%`) based on calibrated propensity scores and recency indicators.
3. **Customer Value & Experience Analysis:** Quantify customer monetary value, installment behavior, review sentiment, and delivery SLA impact across Brazilian states.
4. **Actionable Decision Support:** Deliver reproducible code, automated quality tests, and a bilingual interactive dashboard (`EN / AR`) with one-click CRM CSV export.

---

## 5. Dataset Overview
- **Dataset Name:** Olist Brazilian E-Commerce Public Dataset
- **Source:** `https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce`
- **Validated Scale & Coverage:** All **9 relational CSV files** were verified (`99,441` total orders; **`98,666` qualifying orders** after excluding `canceled` and `unavailable` statuses; **`96,096` unique customers**; **`R$ 15.84M`** item revenue).
- **Entity Grain Resolution:** Confirmed that `customer_id` is generated per order (`99,441` records), whereas **`customer_unique_id`** (`96,096` records) uniquely identifies individuals across repeat purchases and was enforced across all SQL queries and ML pipelines.

| File Name | Role in Pipeline |
|---|---|
| `olist_customers_dataset.csv` | Maps per-order `customer_id` to persistent `customer_unique_id`, city, and state |
| `olist_orders_dataset.csv` | Order statuses and 5 lifecycle timestamps (purchase, approval, carrier, customer delivery, estimated delivery) |
| `olist_order_items_dataset.csv` | Line-item prices (`R$`), freight values, product IDs, and seller IDs |
| `olist_order_payments_dataset.csv` | Payment methods (`credit_card`, `boleto`, `voucher`), installment counts, and payment totals |
| `olist_order_reviews_dataset.csv` | 1–5 star customer satisfaction ratings and review comments |
| `olist_products_dataset.csv` | Product dimensions, weight, and Portuguese category names |
| `olist_sellers_dataset.csv` | Seller location attributes (city and state) |
| `olist_geolocation_dataset.csv` | Brazilian ZIP-code prefix latitude/longitude coordinates |
| `product_category_name_translation.csv` | Maps Portuguese product categories to standardized English names |

---

## 6. Data Validation and Preparation
Implemented in `notebooks/01_data_validation_and_profiling.ipynb` and `notebooks/02_data_cleaning_and_eda.ipynb`:
- **Schema & Cardinality Profiling:** Audited row counts, null percentages, duplicate records, and primary/foreign key integrity, exporting audit tables to `data/profiling_reports/`.
- **Order Qualification Rule:** Excluded `canceled` and `unavailable` orders (`775` orders) to prevent distorted revenue and false repeat counts, retaining **`98,666` qualifying orders**.
- **Standardization & Cleaning:** Parsed all timestamp columns, normalized city/state strings, imputed missing product dimensions with column medians, mapped English category translations, and deduplicated geolocation records by `geolocation_zip_code_prefix` using median coordinates.
- **Reproducibility:** Raw files remain untouched in `data/raw/`, while cleaned relational tables are persisted to `data/cleaned/`.

---

## 7. Finalized Business Definitions
- **Qualifying Order:** Any order in `orders_clean` where `order_status NOT IN ('canceled', 'unavailable')`.
- **Point-in-Time Cutoff Date:** **`2018-03-01`**, selected to preserve a complete `180-day` forward observation window (`2018-03-01` to `2018-08-28`) prior to dataset end (`2018-09`), yielding **`52,013` eligible customers**.
- **Repeat Purchase Target (`target_repeat_180d`):** Binary target (`1` if `customer_unique_id` placed `>= 1` qualifying order between `2018-03-01` and `2018-08-28`; `0` otherwise). Validated baseline repeat rate = **`1.14%`**.
- **Customer Value & SLA Metrics (`src/business_metrics.sql`):** Defined SQL formulas for Qualifying Orders, Unique Customers, Total Item Revenue (`R$`), Total Freight (`R$`), Average Order Value (AOV), Historical Repeat Rate, RFM (`recency_days`, `frequency`, `monetary_total`), and Delivery Delay (`delay_vs_est_days`).
- **Prediction Unit:** One row per `customer_unique_id` evaluated at snapshot date `2018-03-01` (`52,013` rows × `32` features in `data/cleaned/ml_customer_dataset.csv`).

---

## 8. Machine Learning Approach & Validated Results
Implemented in `src/build_ml_dataset.py` and `notebooks/03_ml_modeling_and_evaluation.ipynb`:
- **Leakage Prevention:** Strictly filtered all historical features to `order_purchase_timestamp < '2018-03-01'` and verified via automated assertions in `tests/test_data_quality.py`.
- **Temporal Holdout Split:** Sorted eligible customers chronologically by `last_purchase` using an **80% train (`41,610` customers) / 20% untouched temporal holdout test (`10,403` customers)** split.
- **Model Comparison & Selection (`threshold = 0.60`):**
  - **Champion — `LogisticRegression_balanced` (`C=0.1`, `class_weight='balanced'`):** Selected for superior ranking concentration and probability calibration, achieving **Top-1% Decile Lift = `3.33x`** over the `1.14%` baseline, **PR-AUC = `0.0170`**, **ROC-AUC = `0.5833`**, and **Recall@0.60 = `15.97%`**.
  - **Challenger — `RandomForest_balanced` (`n_estimators=200`, `max_depth=8`, `class_weight='balanced'`):** Evaluated as a non-linear benchmark; outperformed by regularized logistic regression on temporal holdout ranking stability.
- **Operational CRM Propensity Tiers (`models/customer_propensity_scores.csv`):**
  - **High Propensity (Top 5% — `2,601` customers):** Mean repeat probability **`72.1%`** — priority VIP loyalty & personalized cross-sell offers.
  - **Medium Propensity (Next 15% — `7,802` customers):** Mean repeat probability **`59.0%`** — automated win-back nudges & installment reminders.
  - **Low Propensity (Bottom 80% — `41,610` customers):** Mean repeat probability **`42.6%`** — low-cost organic lifecycle touchpoints.
- **Limitations:** Feature contributions indicate behavioral correlation (recency, frequency, satisfaction, delivery timeliness) rather than causal proof; campaign uplift requires A/B testing prior to full-scale budget rollout.

---

## 9. Scope and Boundaries
**Delivered Scope**
- Dataset inspection, schema audit, and data dictionary (`docs/data_dictionary.md`).
- Reproducible data cleaning and exploratory data analysis (`notebooks/02_data_cleaning_and_eda.ipynb`).
- SQL business metric definitions (`src/business_metrics.sql`).
- Point-in-time feature engineering (`src/build_ml_dataset.py`), ML modeling (`notebooks/03_ml_modeling_and_evaluation.ipynb`), and automated data-quality tests (`tests/test_data_quality.py`).
- Interactive decision-support dashboard (`dashboard/app.py` and `dashboard/web_dashboard/index.html`).
- Documented GitHub repository (`custiq-force/`).

**Out of Scope**
- Real-time production e-commerce ERP/CRM API integration.
- Automated outbound email/SMS execution.
- Causal uplift claims without randomized controlled experiments.

---

## 10. Team Structure and Responsibilities
| Team Member | Primary Workstream & Deliverables |
|---|---|
| **Mohanned Mohammed Galal** | Project Lead; SQL queries (`src/business_metrics.sql`), Business Metrics & GitHub coordination |
| **Shahd Magdy Abdelwahd** | Dataset preparation, schema profiling (`notebooks/01_data_validation_and_profiling.ipynb`) & data dictionary |
| **Marwa Elbadawy Mohammed** | Data cleaning, geolocation deduplication & EDA (`notebooks/02_data_cleaning_and_eda.ipynb`) |
| **Yassin Hassan Abdelkader** | Temporal feature store (`src/build_ml_dataset.py`), ML modeling & evaluation (`notebooks/03_ml_modeling_and_evaluation.ipynb`) |
| **Mohammed Atef Mosa** | Interactive dashboard (`dashboard/app.py` & `dashboard/web_dashboard/index.html`), CRM segmentation & recommendations |

---

## 11. Executed End-to-End Workflow
1. **Schema & Grain Validation:** Verified all 9 Olist CSV files and key cardinalities in `01_data_validation_and_profiling.ipynb`.
2. **Data Cleaning & EDA:** Standardized tables, filtered canceled/unavailable orders, and analyzed revenue/SLA patterns in `02_data_cleaning_and_eda.ipynb`.
3. **SQL Business Metrics:** Authored reusable queries for qualifying orders, revenue, repeat rate, and RFM snapshots in `src/business_metrics.sql`.
4. **Point-in-Time Feature Engineering:** Built the 32-feature customer matrix at cutoff `2018-03-01` via `src/build_ml_dataset.py`.
5. **Model Training & Scoring:** Trained `LogisticRegression_balanced` vs. `RandomForest_balanced` on an 80/20 temporal split, saved `models/repeat_purchase_model.joblib`, and scored all `52,013` customers in `03_ml_modeling_and_evaluation.ipynb`.
6. **Automated Quality Verification:** Validated zero leakage (`last_purchase < 2018-03-01`) and valid score bounds via `pytest tests/`.
7. **Dashboard Delivery:** Deployed the bilingual decision-support portal via `dashboard/app.py` and `dashboard/web_dashboard/index.html`.

---

## 12. Technology Stack
| Tool / Library | Role in Project |
|---|---|
| **Python 3.10+** | Core programming language for ETL, feature engineering, modeling, and testing |
| **Pandas & NumPy** | Relational data wrangling, temporal aggregations, and feature matrix construction |
| **SQL** | Business KPI definitions, repeat-rate cohort queries, and RFM extraction (`src/business_metrics.sql`) |
| **Scikit-learn & Joblib** | Preprocessing pipelines (`ColumnTransformer`), model training, evaluation, and model serialization |
| **Matplotlib & Seaborn** | Exploratory data analysis and diagnostic visualizations |
| **Streamlit & HTML/JS/SVG** | Interactive dashboard entrypoint (`dashboard/app.py`) and standalone bilingual web portal (`dashboard/web_dashboard/index.html`) |
| **Pytest & Jupyter** | Automated leakage/schema unit testing and reproducible analytical notebooks |
| **GitHub** | Version control, collaboration, and project documentation |

---

## 13. Dashboard Architecture & Views
Delivered as both a **Streamlit application** (`streamlit run dashboard/app.py`) and a **standalone interactive web portal** (`dashboard/web_dashboard/index.html`) supporting **English and Arabic (`EN / AR`)**:
- **Executive KPI Overview:** Qualifying orders (`98,666`), unique customers (`96,096`), item revenue (`R$ 15.84M`), baseline 180-day repeat rate (`1.14%`), and Top-1% decile lift (`3.33x`).
- **Propensity Tier Breakdown:** Visualizes customer counts and mean repeat probabilities across High (`5%`), Medium (`15%`), and Low (`80%`) propensity tiers.
- **Model Diagnostics:** Displays temporal holdout comparison metrics (`PR-AUC`, `ROC-AUC`, `Recall@0.60`, `Top-1% Lift`).
- **Interactive Filtering & CRM Export:** Allows filtering customer cohorts by Brazilian state and propensity tier with one-click CSV export for marketing execution.

---

## 14. Repository Structure
```text
custiq-force/
├── README.md
├── requirements.txt
├── docs/
│   ├── project_documentation.md                  # Final project report & methodology
│   └── data_dictionary.md                        # Schema definitions & metric formulas
├── data/
│   ├── raw/                                      # Original 9 Olist CSV files
│   ├── cleaned/                                  # Standardized relational tables & ML dataset
│   └── profiling_reports/                        # Automated table & column audit reports
├── notebooks/
│   ├── 01_data_validation_and_profiling.ipynb    # Schema audit & PK/FK cardinality checks
│   ├── 02_data_cleaning_and_eda.ipynb            # Cleaning, geo deduplication & EDA
│   └── 03_ml_modeling_and_evaluation.ipynb       # Temporal holdout training & scoring
├── src/
│   ├── build_ml_dataset.py                       # Point-in-time feature store (2018-03-01 cutoff)
│   └── business_metrics.sql                      # SQL definitions for GMV, RFM & repeat rate
├── models/                                       # Saved .joblib model, metrics & propensity scores
├── dashboard/
│   ├── app.py                                    # Streamlit dashboard entrypoint
│   └── web_dashboard/
│       └── index.html                            # Interactive bilingual dashboard (EN / AR)
└── tests/
    └── test_data_quality.py                      # Automated leakage & score range checks
