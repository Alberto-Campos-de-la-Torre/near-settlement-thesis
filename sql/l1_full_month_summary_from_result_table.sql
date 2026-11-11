-- The exact aggregation that produced the committed data/bigquery/l1_full_month_summary.csv (months 2024-11 .. 2026-01), run on 2026-11-08 as job
-- redacted-private-execution-id over the anonymous result table of the per-account query (job redacted-private-execution-id,
-- 148.2 GB, 45,926,806 rows, never downloaded). Anonymous result tables expire after 24 hours, so this file documents provenance; to rebuild the
-- same aggregate from the public table use l1_full_month_summary.sql.
WITH c AS (
  SELECT *, CASE WHEN ENDS_WITH(account, '.tg') THEN 'tg' WHEN ENDS_WITH(account, '.sweat') THEN 'sweat' WHEN ENDS_WITH(account, '.kaiching') THEN 'kaiching'
                 WHEN REGEXP_CONTAINS(account, r'^[0-9a-f]{64}$') THEN 'implicit' WHEN REGEXP_CONTAINS(account, r'^0x[0-9a-f]{40}$') THEN 'eth_implicit'
                 WHEN ENDS_WITH(account, '.near') THEN 'named' ELSE 'other' END AS fine_class
  FROM `your-project-id.your_dataset.source_results`)
SELECT month, fine_class AS name_class, COUNT(*) AS accounts, COUNTIF(txns = 1) AS single_tx_accounts, COUNTIF(distinct_receivers >= 2) AS multi_receiver_accounts,
       COUNTIF(intents_txns > 0) AS intents_accounts, SUM(txns) AS txns, AVG(active_days) AS active_days_mean, APPROX_QUANTILES(txns, 100)[OFFSET(50)] AS txns_median
FROM c GROUP BY month, name_class ORDER BY month, name_class;
