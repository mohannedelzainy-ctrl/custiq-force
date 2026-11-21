-- Custiq Force: Core Business Metrics & Customer Retention Queries
-- Author: Mohanned Mohammed Galal (Project Lead — SQL & Business Metrics)

SELECT
    COUNT(DISTINCT o.order_id) AS qualifying_orders,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers,
    ROUND(SUM(oi.price), 2) AS total_item_revenue_brl,
    ROUND(SUM(oi.freight_value), 2) AS total_freight_brl,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS average_order_value_brl
FROM orders_clean o
JOIN customers_clean c ON o.customer_id = c.customer_id
JOIN order_items_clean oi ON o.order_id = oi.order_id
WHERE o.order_status NOT IN ('canceled', 'unavailable');

WITH customer_order_counts AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM orders_clean o
    JOIN customers_clean c ON o.customer_id = c.customer_id
    WHERE o.order_status NOT IN ('canceled', 'unavailable')
    GROUP BY c.customer_unique_id
)
SELECT
    COUNT(*) AS total_unique_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(AVG(CASE WHEN order_count > 1 THEN 1.0 ELSE 0.0 END) * 100, 2) AS repeat_rate_pct
FROM customer_order_counts;

SELECT
    c.customer_unique_id,
    c.customer_state,
    DATEDIFF('2018-03-01', MAX(o.order_purchase_timestamp)) AS recency_days,
    COUNT(DISTINCT o.order_id) AS frequency,
    ROUND(SUM(oi.price), 2) AS monetary_total,
    ROUND(AVG(r.review_score), 2) AS avg_review_score
FROM orders_clean o
JOIN customers_clean c ON o.customer_id = c.customer_id
LEFT JOIN order_items_clean oi ON o.order_id = oi.order_id
LEFT JOIN order_reviews_clean r ON o.order_id = r.order_id
WHERE o.order_status NOT IN ('canceled', 'unavailable')
  AND o.order_purchase_timestamp < '2018-03-01'
GROUP BY c.customer_unique_id, c.customer_state;
