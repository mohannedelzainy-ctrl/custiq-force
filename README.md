# Custiq Force

## E-commerce Customer Intelligence & Retention

**DEPI Graduation Project — Data Science**

| Field | Details |
|---|---|
| Program | DEPI Graduation Project — Data Science |
| Supervisor | Eng. Ahmed Mostafa |
| Submission Date | 6 December 2026 |
| Dataset | Olist Brazilian E-Commerce Public Dataset |
| Document Status | Draft v0.2 — Machine learning included; detailed decisions pending |

## 1. Executive Summary

Custiq Force is an E-commerce AI and Data Science project intended to turn customer and transaction data into actionable business insights. Its planned focus is repeat-purchase prediction, customer value analysis, identifying customers who may be at risk of not returning, and providing data-informed recommendations to support customer retention.

The selected source is the Olist Brazilian E-Commerce Public Dataset. The team will inspect the actual downloaded files, verify their schema and quality, and then finalize business definitions, analytical methods, and predictive targets. No model performance or business findings are claimed before analysis is completed.

## 2. Project Information

| Program | DEPI Graduation Project — Data Science |
|---|---|
| Supervisor | Eng. Ahmed Mostafa |
| Submission Date | 6 December 2026 |
| Dataset | Olist Brazilian E-Commerce Public Dataset |
| Document Status | Draft v0.2 — Machine learning included; detailed decisions pending |

## 3. Background and Business Problem

E-commerce businesses can use customer and transaction history to better understand purchasing behavior and prioritize retention efforts. Without structured analysis, it can be difficult to identify valuable customers, recognize changes in purchase activity, or determine which customers may benefit from targeted engagement.

Custiq Force aims to provide an analytical workflow that connects customer data with interpretable insights and practical recommendations. The exact analytical scope will be confirmed after the dataset is reviewed.

## 4. Project Objectives

- Estimate the likelihood that a customer will make another purchase, if the data supports a defensible target and evaluation design.
- Identify customers who may be at risk of not returning using an agreed, time-based definition of inactivity.
- Analyze customer value using suitable measures supported by the dataset.
- Provide evidence-based recommendations for customer retention and business decision-making.

## 5. Dataset Overview

Dataset name: Olist Brazilian E-Commerce Public Dataset.

Source page: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

The dataset is a multi-table snapshot of Brazilian e-commerce orders and related entities. It is commonly described as covering roughly 100,000 orders placed between 2016 and 2018. The team must confirm exact record counts, date coverage, and available columns from its downloaded files before including these figures in final reporting.

Important modeling note: customer_id generally identifies a customer record associated with an order, while customer_unique_id is intended to link repeat activity for the same underlying customer. Repeat-purchase analysis should investigate customer_unique_id rather than assuming customer_id alone identifies a person across orders.

| olist_customers_dataset.csv | Customer records; includes customer_id and customer_unique_id |
|---|---|
| olist_orders_dataset.csv | Order status and timestamps |
| olist_order_items_dataset.csv | Order items, product/seller references, price and freight |
| olist_order_payments_dataset.csv | Payment information for orders |
| olist_order_reviews_dataset.csv | Customer review information |
| olist_products_dataset.csv | Product attributes and category |
| olist_sellers_dataset.csv | Seller records |
| olist_geolocation_dataset.csv | Brazilian ZIP-code geolocation data |
| product_category_name_translation.csv | Portuguese-to-English product category translation |

These are the commonly supplied dataset components. Verify which files are present in the team's download; do not assume every file is included or complete.

## 6. Data Validation and Preparation

- Record actual file names, row counts, column counts, data types, and date coverage.
- Inspect missing values, duplicates, invalid timestamps, unusual values, and key uniqueness.
- Understand the grain of each table: customer, order, order item, payment, review, product, seller, or geolocation record.
- Check join keys and relationship cardinalities before combining tables to avoid duplicated orders or inflated revenue.
- Review order statuses and define which orders qualify for each metric.
- Document the data dictionary, assumptions, limitations, license, and permitted use.
- Keep raw data unchanged and make preparation reproducible through scripts or notebooks.

## 7. Business Definitions to Finalize

The following are proposed work items, not finalized definitions:

- Repeat purchase: a customer places a subsequent qualifying order after a defined cutoff date.
- Customer at risk: a customer has not placed a qualifying order within a justified inactivity window. The window must be selected after examining the date range and purchase cadence.
- Customer value: choose supported measures such as purchase frequency, recency, and qualifying order value; document treatment of canceled orders, freight, and payment records.
- Business metrics: candidate measures include qualifying orders, repeat-customer rate, average order value, purchase frequency, recency, and revenue summaries. Exact formulas must be documented.
- Prediction unit: define whether each modeling row represents a customer at a snapshot date or another unit.

## 8. Machine Learning Approach

Machine learning is an explicit component of Custiq Force. The team will define a valid prediction target from the dataset, create customer-level features, train and compare suitable models, evaluate results, and interpret model behavior. The final target, model algorithms, and metrics will be chosen after dataset validation rather than assumed in advance.

### Planned ML workflow

1. Define the business question and prediction unit.
2. Create a time-aware target and observation window, if supported by available timestamps.
3. Build features using only information available at the prediction cutoff.
4. Create a baseline model and then compare suitable alternatives.
5. Evaluate on held-out data; consider a time-based split to reflect future use.
6. Review errors, class balance, and metric trade-offs.
7. Interpret predictions and document limitations before turning results into recommendations.

### Potential evaluation metrics

For a classification task, candidate metrics include precision, recall, F1-score, ROC-AUC, and a confusion matrix. The team should select metrics based on class balance and business priorities; accuracy alone may be misleading. Probability calibration may matter if predicted probabilities are used to prioritize customers.

### Leakage and explainability

Features must not contain information from after the prediction cutoff. Model interpretation can describe patterns and feature contributions, but feature importance does not prove causation. The final documentation should report the chosen method, evaluation results, limitations, and the meaning of predictions in business terms.

## 9. Scope and Boundaries

### Planned scope

- Dataset inspection and data dictionary.
- Data cleaning and exploratory data analysis (EDA).
- SQL queries and business metrics.
- Machine-learning experiments, evaluation, and interpretation.
- Streamlit dashboard for selected metrics, analyses, model outputs, and recommendations.
- GitHub repository with documented code, workflow, and project files.

### Out of scope unless approved later

- Live integration with a production e-commerce platform.
- Automated marketing campaigns or direct customer messaging.
- Claims that recommendations cause business improvements without an appropriate experiment.
- Predictions or features unsupported by the available data.

## 10. Team Structure and Responsibilities

Task ownership identifies each member's primary responsibility, not isolated work. The team will learn together and review code, assumptions, and results across stages.

| Mohanned Mohammed Galal | Project Lead; SQL, Business Metrics, GitHub coordination |
|---|---|
| Shahd Magdy Abdelwahd | Dataset preparation and database setup |
| Marwa Elbadawy Mohammed | Data cleaning, EDA, customer behavior analysis |
| Yassin Hassan Abdelkader | Machine learning, model evaluation, and interpretation |
| Mohammed Atef Mosa | Streamlit dashboard, results, and recommendations |

## 11. Proposed End-to-End Workflow

1. Inventory dataset files and review source/license conditions.
2. Understand table grain, columns, keys, date coverage, and business context.
3. Design the relational database and load appropriate tables into MySQL, if suitable.
4. Perform data quality checks, cleaning, and EDA using Python, Pandas, Matplotlib, and Seaborn.
5. Create customer-level features and business metrics with SQL/Python; document formulas.
6. Define repeat-purchase and at-risk targets using time-aware logic where feasible.
7. Train a baseline machine-learning model and compare appropriate alternatives.
8. Evaluate and interpret model results; record limitations.
9. Build the Streamlit dashboard and connect it to validated analysis outputs.
10. Review the complete workflow, document setup instructions, and prepare the final presentation.

## 12. Technology Stack

| Python | Data analysis, feature engineering, and modeling |
|---|---|
| Pandas | Tabular data loading and transformation |
| SQL / MySQL | Data querying, joins, and business metrics |
| Scikit-learn | Model pipelines, training, and evaluation |
| Matplotlib / Seaborn | Exploratory and explanatory visualizations |
| Streamlit | Interactive dashboard |
| GitHub | Version control, collaboration, issues, and documentation |

## 13. Dashboard Plan

The Streamlit dashboard is planned to present a selected subset of validated outputs. Candidate views include overall order/customer metrics, repeat-purchase patterns, customer value analysis, at-risk customer indicators, model evaluation, and recommendations. Final pages and filters will be decided after the dataset and analysis are understood.

## 14. GitHub and Collaboration

- Keep a README with project purpose, dataset source, setup instructions, and current status.
- Use a clear folder structure for data notes, notebooks, source code, dashboard, and documentation.
- Do not commit credentials or private information. Check dataset redistribution terms before uploading raw data.
- Use descriptive commits and review changes before merging into the main branch.
- Track decisions, unresolved questions, and task ownership in GitHub Issues or a shared task board.

```text
custiq-force/\n├── README.md\n├── docs/\n│   ├── project_documentation.md\n│   └── data_dictionary.md\n├── data/\n│   └── README.md\n├── notebooks/\n├── src/\n├── dashboard/\n├── tests/\n└── requirements.txt
```

## 15. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| Customer identity confusion | Validate customer_unique_id for customer-level repeat behavior. |
| Data leakage | Define a prediction cutoff; exclude future-derived features; use time-based evaluation where feasible. |
| Join duplication | Document table grain and test row counts and key cardinalities after joins. |
| Ambiguous churn definition | Agree on and justify an inactivity window; state that it is a project definition. |
| Class imbalance | Inspect target distribution and report metrics beyond accuracy. |
| Overstated recommendations | Separate prediction/correlation from causation and document limitations. |
| Scope creep | Prioritize a working end-to-end baseline before optional features. |

## 16. Deliverables

- Dataset inventory and data dictionary.
- Reproducible data preparation and EDA outputs.
- SQL queries and documented business metric definitions.
- Machine-learning model(s), evaluation results, and interpretation.
- Streamlit dashboard.
- GitHub repository with README and setup instructions.
- Final presentation and project documentation.

## 17. Timeline and Milestones

Submission date supplied by the team: 6 December 2026. Intermediate dates have not been supplied, so milestones are listed without invented deadlines.

1. Dataset validation and project scope confirmation.
2. Database setup and data preparation.
3. EDA and business metric definitions.
4. Target definition, feature engineering, baseline modeling, and evaluation.
5. Dashboard development and integration.
6. Testing, documentation review, and final presentation.

## 18. Open Decisions

- Confirm exact downloaded files and row counts.
- Confirm whether Custiq Force is the final project name.
- Define qualifying order statuses and treatment of canceled/unavailable orders.
- Choose prediction cutoff, future window, and repeat-purchase definition.
- Choose and justify the inactivity window for identifying customers at risk.
- Finalize customer value formula and business metric definitions.
- Select model candidates and evaluation metrics after inspecting the target.
- Confirm GitHub repository URL and whether raw data may be shared.

## 19. Conclusion

Custiq Force will use the Olist Brazilian E-Commerce Public Dataset as the starting point for a collaborative Data Science workflow. Machine learning is a core part of the project alongside SQL, business analysis, data preparation, and dashboard development. The project will prioritize data understanding, valid business definitions, careful evaluation, and clear recommendations. Final conclusions will be added only after the team analyzes the actual data.

