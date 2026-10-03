-- 01_staging_and_quality.sql
-- ANSI-style reference SQL; adapt DATE/QUALIFY syntax to your warehouse.

CREATE OR REPLACE VIEW stg_shipments_dedup AS
WITH ranked AS (
    SELECT s.*,
           ROW_NUMBER() OVER (PARTITION BY shipment_id ORDER BY ingestion_ts DESC) AS rn
    FROM raw_universal_shipments s
)
SELECT * EXCLUDE (rn)
FROM ranked
WHERE rn = 1;

CREATE OR REPLACE VIEW dq_shipments AS
SELECT
  COUNT(*) AS row_count,
  SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS missing_customer_id,
  SUM(CASE WHEN weight_lbs IS NULL THEN 1 ELSE 0 END) AS missing_weight,
  SUM(CASE WHEN weight_lbs <= 0 THEN 1 ELSE 0 END) AS nonpositive_weight,
  SUM(CASE WHEN freight_class NOT IN
      (50,55,60,65,70,77.5,85,92.5,100,110,125,150,175,200,250,300,400,500)
      THEN 1 ELSE 0 END) AS invalid_freight_class
FROM stg_shipments_dedup;

-- Production note:
-- repairs should be written to a curated table with repair_reason and original_value
-- rather than silently overwriting source fields.
