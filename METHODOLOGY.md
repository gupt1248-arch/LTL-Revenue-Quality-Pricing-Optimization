# Methodology and Assumptions

## 1. Scope
This is a synthetic LTL revenue-quality decision-support project. It demonstrates how an analyst could combine shipment, customer, contract, lane, freight-class, accessorial, fuel, pricing and cost data to identify revenue leakage and prioritize commercial action.

## 2. Public grounding vs. synthetic assumptions
The operating concepts are grounded in public FedEx materials, but the numerical model is synthetic.

Publicly grounded concepts:
- FedEx Freight's 2022 Space and Pace pilot used shipment weight, dimensions, origin ZIP and destination ZIP, with DIM verification, and was positioned as a way to improve pricing accuracy and reduce backend adjustments/disputes.
- Public FedEx freight rate pages show freight rating concepts such as service type, freight class, weight, discounts, declared value and accessorial services.
- FedEx's 2022 annual report discussed list-price increases, surcharges and an indexed fuel surcharge for FedEx Freight.
- A 2008 FedEx newsroom release publicly identified Dillard's as using FedEx Freight / FedEx National LTL.

Synthetic assumptions:
- All shipment-level values, contracts, discounts, costs, revenue, elasticity and account behavior.
- Terminal-to-terminal distance uses geographic distance with a road-factor approximation.
- Cost-to-serve is a simplified analytical proxy, not a carrier cost-accounting model.
- Expected revenue is generated from class, weight, distance, service, discount, fuel and accessorial logic.
- Pricing elasticity is illustrative and must be estimated from actual historical price/volume behavior before production use.

## 3. Data-quality defects intentionally injected
The raw dataset includes duplicate shipment rows, missing/non-positive weights, invalid freight classes and missing customer IDs. ETL repairs them with deterministic rules and produces an auditable before/after report.

## 4. Commercial leakage intentionally injected
Six major mechanisms are included:
1. Outdated contract discount.
2. Long-haul lane underpricing.
3. Freight-class mismatch.
4. Missing accessorial charges.
5. Excess discretionary discount.
6. Lane-specific pricing gap.

These are synthetic labels used to validate whether the analysis can recover planted problems.

## 5. Revenue-quality measures
- Pricing realization = billed revenue / expected revenue.
- Revenue gap = max(expected revenue - billed revenue, 0).
- Revenue/CWT = billed revenue / (weight lbs / 100).
- Contribution = billed revenue - estimated cost.
- Contribution margin = contribution / billed revenue.

## 6. Predictive model
A HistGradientBoostingRegressor is trained on near-normal shipments to estimate expected revenue from observable shipment and commercial features. Categorical variables are one-hot encoded. Holdout MAE and R² are reported. The model is used for anomaly prioritization; it does not determine final prices.

## 7. Pricing simulation
Customer-lane cells with sufficient shipment count and weak realization are selected. Scenarios from +1% to +5% are simulated using illustrative negative volume elasticity. The objective is incremental contribution, not gross revenue.

## 8. Recommended production controls
- Replace synthetic expected-rate logic with governed contract/rating tables.
- Estimate elasticity by customer/segment/lane using causal or quasi-experimental methods where possible.
- Separate billing defects from commercially approved discounts.
- Add confidence intervals and minimum-support thresholds.
- Require pricing/finance approval before customer action.
- Measure pilots with test/control or matched-control cohorts.

## Public sources
- FedEx Freight Space and Pace pilot: https://newsroom.fedex.com/newsroom/global-english/fedex-freight-launches-space-and-pace-pilot
- FedEx Freight rate information: https://fedexfreight.fedex.com/ratecentral.jsp
- FedEx 2022 Annual Report: https://investors.fedex.com/files/doc_financials/2022/ar/Annual-Report.pdf
- Historical Dillard's reference: https://newsroom.fedex.com/newsroom/united-states-english/fedex-significantly-improves-less-than-truckload-ltl-services
