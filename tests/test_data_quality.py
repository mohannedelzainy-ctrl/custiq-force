import os
import pandas as pd

def test_no_data_leakage_cutoff():
    path = "03_machine_learning/ml_data/ml_customer_dataset.csv"
    if not os.path.exists(path):
        return
    df = pd.read_csv(path)
    assert (pd.to_datetime(df["last_purchase"]) < pd.Timestamp("2018-03-01")).all(), "Leakage detected: purchase >= cutoff!"
    assert (df["recency_days"] > 0).all(), "Recency must be strictly positive!"

def test_propensity_scores_valid():
    path = "03_machine_learning/model_artifacts/customer_propensity_scores.csv"
    if not os.path.exists(path):
        return
    scores = pd.read_csv(path)
    assert scores["predicted_repeat_probability"].between(0, 1).all(), "Probabilities must be in [0, 1]"
    assert set(scores["propensity_segment"].unique()) == {"High (top 5%)", "Medium (next 15%)", "Low (bottom 80%)"}
