-- Revenue leakage summary
SELECT
    COUNT(*) AS rows,
    SUM(CASE WHEN isleakage THEN 1 ELSE 0 END) AS leakage_rows,
    SUM(revenue) AS net_revenue,
    SUM(CASE WHEN isleakage THEN revenue ELSE 0 END) AS leakage_revenue,
    SUM(CASE WHEN NOT isleakage THEN revenue ELSE 0 END) AS postive_revenue
FROM retail_clean

-- Leakage by country
SELECT
    country,
    SUM(revenue) AS net_revenue,
    SUM(CASE WHEN isleakage THEN revenue ELSE 0 END) AS leakage_revenue
FROM retail_clean
GROUP BY 1
ORDER BY leakage_revenue ASC;