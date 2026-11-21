"""Build the leakage-aware customer snapshot for Custiq Force."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "01_Data_Collection" / "raw_data"
OUT = HERE / "ml_data"
OUT.mkdir(parents=True, exist_ok=True)

SNAPSHOT_DATE = pd.Timestamp("2018-03-01")
HORIZON_DAYS = 180
WINDOW_END = SNAPSHOT_DATE + pd.Timedelta(days=HORIZON_DAYS)


def load(name: str) -> pd.DataFrame:
    return pd.read_csv(RAW / name)


def main() -> None:
    orders = load("olist_orders_dataset.csv")
    customers = load("olist_customers_dataset.csv")
    items = load("olist_order_items_dataset.csv")
    payments = load("olist_order_payments_dataset.csv")
    reviews = load("olist_order_reviews_dataset.csv")
    products = load("olist_products_dataset.csv")

    for col in [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")

    reviews["review_creation_date"] = pd.to_datetime(
        reviews["review_creation_date"], errors="coerce"
    )

    order_base = orders.merge(
        customers[
            [
                "customer_id",
                "customer_unique_id",
                "customer_state",
                "customer_city",
                "customer_zip_code_prefix",
            ]
        ],
        on="customer_id",
        how="left",
        validate="many_to_one",
    )

    # Strict temporal boundary: only delivered orders completed before SNAPSHOT_DATE
    past = order_base[
        (order_base["order_purchase_timestamp"] < SNAPSHOT_DATE)
        & (order_base["order_status"] == "delivered")
        & (order_base["order_delivered_customer_date"] < SNAPSHOT_DATE)
    ].copy()

    future = order_base[
        (order_base["order_purchase_timestamp"] >= SNAPSHOT_DATE)
        & (order_base["order_purchase_timestamp"] < WINDOW_END)
        & (order_base["order_status"] == "delivered")
    ].copy()

    past_ids = set(past["order_id"])

    # Order-level item features
    historical_items = items[items["order_id"].isin(past_ids)].merge(
        products[["product_id", "product_category_name"]],
        on="product_id",
        how="left",
        validate="many_to_one",
    )
    item_features = (
        historical_items.groupby("order_id")
        .agg(
            item_count=("order_item_id", "count"),
            order_item_value=("price", "sum"),
            freight_value=("freight_value", "sum"),
            unique_products=("product_id", "nunique"),
            unique_sellers=("seller_id", "nunique"),
            category_diversity=("product_category_name", "nunique"),
        )
        .reset_index()
    )

    # Order-level payment features
    payment_features = (
        payments[payments["order_id"].isin(past_ids)]
        .groupby("order_id")
        .agg(
            payment_value=("payment_value", "sum"),
            payment_installments_max=("payment_installments", "max"),
        )
        .reset_index()
    )

    history = (
        past.merge(item_features, on="order_id", how="left")
        .merge(payment_features, on="order_id", how="left")
        .sort_values("order_purchase_timestamp")
    )

    history["order_total_value"] = history["payment_value"].fillna(
        history["order_item_value"].fillna(0)
    )
    history["delivery_days"] = (
        history["order_delivered_customer_date"] - history["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400.0
    history["delivery_delay_days"] = (
        history["order_delivered_customer_date"] - history["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400.0
    history["is_late_delivery"] = (history["delivery_delay_days"] > 0).astype(int)

    # Eligible reviews created strictly before SNAPSHOT_DATE
    eligible_reviews = reviews[
        reviews["order_id"].isin(past_ids)
        & (reviews["review_creation_date"] < SNAPSHOT_DATE)
    ].copy()
    eligible_reviews["review_score"] = pd.to_numeric(
        eligible_reviews["review_score"], errors="coerce"
    )
    review_features = (
        eligible_reviews.groupby("order_id")
        .agg(order_review_score=("review_score", "mean"))
        .reset_index()
    )
    history = history.merge(review_features, on="order_id", how="left")

    # Customer-level aggregation
    customer_features = (
        history.groupby("customer_unique_id")
        .agg(
            historical_orders=("order_id", "nunique"),
            historical_spend=("order_total_value", "sum"),
            avg_order_value=("order_total_value", "mean"),
            median_order_value=("order_total_value", "median"),
            max_order_value=("order_total_value", "max"),
            total_items=("item_count", "sum"),
            avg_items_per_order=("item_count", "mean"),
            total_freight=("freight_value", "sum"),
            avg_freight_per_order=("freight_value", "mean"),
            unique_products=("unique_products", "sum"),
            unique_sellers=("unique_sellers", "sum"),
            avg_category_diversity=("category_diversity", "mean"),
            avg_payment_installments=("payment_installments_max", "mean"),
            avg_delivery_days=("delivery_days", "mean"),
            avg_delivery_delay_days=("delivery_delay_days", "mean"),
            late_delivery_rate=("is_late_delivery", "mean"),
            avg_review_score=("order_review_score", "mean"),
            review_count=("order_review_score", "count"),
            first_purchase=("order_purchase_timestamp", "min"),
            last_purchase=("order_purchase_timestamp", "max"),
            customer_state=(
                "customer_state",
                lambda x: x.dropna().iloc[-1] if x.notna().any() else "unknown",
            ),
            customer_city=(
                "customer_city",
                lambda x: x.dropna().iloc[-1] if x.notna().any() else "unknown",
            ),
        )
        .reset_index()
    )

    customer_features["recency_days"] = (
        SNAPSHOT_DATE - customer_features["last_purchase"]
    ).dt.days
    customer_features["customer_tenure_days"] = (
        SNAPSHOT_DATE - customer_features["first_purchase"]
    ).dt.days
    customer_features["purchase_span_days"] = (
        customer_features["last_purchase"] - customer_features["first_purchase"]
    ).dt.days
    customer_features["orders_per_30_days"] = customer_features["historical_orders"] / (
        customer_features["customer_tenure_days"].clip(lower=30) / 30.0
    )

    # Strictly binary payment method indicators (0/1)
    historical_payments = payments[payments["order_id"].isin(past_ids)][
        ["order_id", "payment_type"]
    ].merge(
        past[["order_id", "customer_unique_id"]],
        on="order_id",
        how="left",
        validate="many_to_one",
    )
    historical_payments["payment_type"] = (
        historical_payments["payment_type"].fillna("unknown").astype(str)
    )
    payment_flags = (
        pd.crosstab(
            historical_payments["customer_unique_id"],
            historical_payments["payment_type"],
        )
        > 0
    ).astype("int8")

    payment_flags.columns = [
        "used_payment_" + str(col).lower().replace(" ", "_").replace("/", "_")
        for col in payment_flags.columns
    ]
    customer_features = customer_features.merge(
        payment_flags.reset_index(), on="customer_unique_id", how="left"
    )
    payment_flag_cols = [
        c for c in customer_features.columns if c.startswith("used_payment_")
    ]
    customer_features[payment_flag_cols] = (
        customer_features[payment_flag_cols].fillna(0).astype("int8")
    )

    # Target label: repeat purchase in [2018-03-01, 2018-08-28)
    future_customers = set(future["customer_unique_id"].dropna().unique())
    customer_features["repeat_purchase_next_180d"] = (
        customer_features["customer_unique_id"].isin(future_customers).astype("int8")
    )
    customer_features["snapshot_date"] = SNAPSHOT_DATE.date().isoformat()
    customer_features["label_window_end"] = WINDOW_END.date().isoformat()
    customer_features = customer_features.drop(columns=["first_purchase", "last_purchase"])

    assert customer_features["customer_unique_id"].is_unique, "customer_unique_id must be unique"
    assert customer_features["repeat_purchase_next_180d"].notna().all(), "Target cannot contain nulls"
    for c in payment_flag_cols:
        assert set(customer_features[c].unique()).issubset({0, 1}), f"{c} must be binary 0/1"

    out_file = OUT / "ml_customer_dataset.csv"
    customer_features.to_csv(out_file, index=False)

    # Update quality report automatically so metadata stays 100% in sync
    q_rows = []
    for col in customer_features.columns:
        miss = int(customer_features[col].isna().sum())
        q_rows.append({
            "column": col,
            "dtype": str(customer_features[col].dtype),
            "rows": len(customer_features),
            "missing_count": miss,
            "missing_pct": round(miss / len(customer_features) * 100, 4),
            "distinct_non_null": int(customer_features[col].nunique(dropna=True))
        })
    pd.DataFrame(q_rows).to_csv(OUT / "ml_dataset_quality_report.csv", index=False)

    print("Saved:", out_file)
    print("Rows:", len(customer_features))
    print("Positive labels:", int(customer_features["repeat_purchase_next_180d"].sum()))
    print("Positive rate:", round(customer_features["repeat_purchase_next_180d"].mean() * 100, 3), "%")


if __name__ == "__main__":
    main()
