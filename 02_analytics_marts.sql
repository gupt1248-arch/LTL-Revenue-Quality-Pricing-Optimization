-- 02_analytics_marts.sql

CREATE OR REPLACE VIEW mart_revenue_quality AS
SELECT
  shipment_id, ship_date, customer_id, customer_name, lane_id,
  billed_revenue, expected_revenue, estimated_cost,
  GREATEST(expected_revenue - billed_revenue, 0) AS revenue_gap,
  billed_revenue / NULLIF(expected_revenue,0) AS pricing_realization,
  billed_revenue / NULLIF(weight_lbs/100.0,0) AS revenue_per_cwt,
  billed_revenue - estimated_cost AS contribution,
  (billed_revenue - estimated_cost) / NULLIF(billed_revenue,0) AS contribution_margin
FROM curated_shipments;

CREATE OR REPLACE VIEW mart_customer_month AS
SELECT
  customer_id,
  DATE_TRUNC('month', ship_date) AS month,
  COUNT(DISTINCT shipment_id) AS shipments,
  SUM(billed_revenue) AS revenue,
  SUM(expected_revenue) AS expected_revenue,
  SUM(GREATEST(expected_revenue-billed_revenue,0)) AS revenue_gap,
  SUM(billed_revenue) / NULLIF(SUM(expected_revenue),0) AS pricing_realization,
  SUM(billed_revenue-estimated_cost) AS contribution
FROM curated_shipments
GROUP BY 1,2;

CREATE OR REPLACE VIEW mart_lane_month AS
SELECT
  lane_id,
  DATE_TRUNC('month', ship_date) AS month,
  COUNT(DISTINCT shipment_id) AS shipments,
  SUM(billed_revenue) AS revenue,
  SUM(GREATEST(expected_revenue-billed_revenue,0)) AS revenue_gap,
  SUM(billed_revenue) / NULLIF(SUM(expected_revenue),0) AS pricing_realization
FROM curated_shipments
GROUP BY 1,2;
