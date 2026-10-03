# Data Dictionary

## `universal_shipments_raw.csv.gz`
| Field | Meaning |
|---|---|
| shipment_id | Synthetic shipment identifier |
| ship_date | Shipment date |
| customer_id / customer_name | Account identifiers; see disclosure in README |
| origin_terminal_id / destination_terminal_id | Synthetic network nodes using real city names |
| lane_id | Origin-destination terminal pair |
| service_level | Priority or Economy |
| weight_lbs | Shipment weight; raw file contains planted DQ defects |
| pallet_count | Synthetic handling-unit count |
| freight_class | NMFC-style class proxy; raw file contains planted invalid values |
| density_lbs_cuft | Synthetic density |
| distance_miles | Approximate lane distance |
| base_discount_pct | Synthetic contract discount |
| fuel_surcharge_pct | Synthetic fuel index-derived surcharge |
| *_flag | Accessorial requirement flags |
| expected_revenue | Synthetic benchmark revenue before leakage |
| billed_revenue | Synthetic realized revenue |
| estimated_cost | Simplified cost-to-serve proxy |
| injected_issue | Ground-truth synthetic commercial problem for validation |
| injected_leakage | Ground-truth planted leakage amount |
| source_system | Synthetic source system |
| ingestion_ts | Synthetic ingestion timestamp |

## Processed metrics
| Field | Meaning |
|---|---|
| revenue_gap | max(expected - billed, 0) |
| pricing_realization | billed / expected |
| revenue_per_cwt | billed / hundredweight |
| contribution | billed - estimated cost |
| contribution_margin | contribution / billed |
| revenue_quality_flag | Threshold-based triage label |
| model_expected_revenue | ML-estimated expected revenue |
| model_gap | model expected - billed, floored at zero |
| model_anomaly_flag | Model gap >= 6% |
