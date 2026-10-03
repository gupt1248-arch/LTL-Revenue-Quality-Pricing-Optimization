# LTL Revenue Quality & Pricing Optimization

An end-to-end **synthetic** revenue-quality analytics case study designed around the responsibilities of a Senior Revenue Quality / Pricing Analyst in less-than-truckload (LTL) freight.

## Executive question
**Where is revenue quality deteriorating, what is causing the leakage, how much is economically actionable, and which targeted pricing interventions should management pilot?**

## Portfolio highlights
- **220,000 unique synthetic LTL shipments** across 2024–2026.
- Raw universal dataset contains deliberately injected **data-quality defects** and **commercial revenue-quality problems**.
- ETL/data-quality layer repairs duplicates, missing/invalid weights, invalid freight classes, and missing customer IDs.
- Shipment-level revenue-quality metrics: pricing realization, revenue/CWT, revenue gap, contribution, contribution margin.
- Root-cause analysis across customers, lanes, freight classes and accessorials.
- Gradient-boosted expected-revenue model: **R² 0.921**, MAE **$52** on the holdout set.
- Targeted customer-lane pricing simulation incorporates illustrative volume elasticity.
- Python/Streamlit dashboard and executive PowerPoint included.

## Important disclosure
This repository is **not FedEx internal work** and contains **no confidential FedEx data**. All shipment, pricing, cost, contract, lane and financial values are synthetic.

**Dillard's** appears only because FedEx publicly identified Dillard's as a user of FedEx Freight / FedEx National LTL in a 2008 FedEx newsroom release. Its shipment records, pricing, economics and behavior in this repository are entirely synthetic and should not be interpreted as current or historical Dillard's data.

All other customer names are fictional. This design is intentional: public sources do not provide a reliable current list of major FedEx Freight customers with account-level economics, so inventing real-company relationships would reduce the credibility of the case study.

## Repository structure
```text
data/
  raw/universal_shipments_raw.csv.gz
  reference/                 # customer, terminal, lane, class, contract, calendar, rate-card references
  processed/                 # cleaned fact, marts, model scores, pricing scenarios
notebooks/
  revenue_quality_end_to_end.ipynb
sql/
  01_staging_and_quality.sql
  02_analytics_marts.sql
dashboard/
  app.py
reports/
  executive_recommendations.pptx
  data_quality_report.csv
  kpi_summary.json
  figures/
src/
  generate_synthetic_data.py
README.md
METHODOLOGY.md
DATA_DICTIONARY.md
requirements.txt
```

## Core business findings from the synthetic case
- Portfolio billed revenue: **$75.8M**
- Identified shipment-level revenue gap: **$1.37M**
- Portfolio pricing realization: **98.79%**
- Revenue-quality flagged shipments: **36,562**
- The leakage is intentionally concentrated in realistic mechanisms: outdated contract discounts, long-haul lane underpricing, freight-class mismatch, missing accessorials, excess discretionary discounting, and lane-specific pricing gaps.
- The recommended operating model is **targeted intervention + 60–90 day test/control measurement**, not a blanket price increase.

## How to run
```bash
pip install -r requirements.txt
jupyter lab notebooks/revenue_quality_end_to_end.ipynb
streamlit run dashboard/app.py
```

## Business interpretation
The model is a prioritization tool, not an autonomous pricing engine. A flagged shipment/account should trigger commercial review. Pricing recommendations should be constrained by contracts, service commitments, competitive context, customer lifetime value and validated elasticity.

## Public grounding
- FedEx Freight described a 2022 **Space and Pace** pricing pilot using weight, dimensions, origin and destination and DIM verification to improve pricing accuracy and reduce adjustments/disputes.
- FedEx public materials describe freight rating inputs including class, weight, discounts and accessorial charges.
- FedEx publicly identified Dillard's as a freight customer in a historical 2008 newsroom release.

Sources are documented in `METHODOLOGY.md`.
