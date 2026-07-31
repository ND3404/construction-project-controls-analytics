-- Process Phase: reusable data-quality checks
PRAGMA foreign_keys = ON;

-- 1. Row counts
SELECT 'projects' AS table_name, COUNT(*) AS row_count FROM projects
UNION ALL
SELECT 'monthly_performance', COUNT(*) FROM monthly_performance
UNION ALL
SELECT 'change_orders', COUNT(*) FROM change_orders
UNION ALL
SELECT 'rfi_log', COUNT(*) FROM rfi_log;

-- 2. Duplicate primary keys (all queries should return zero rows)
SELECT Project_ID, COUNT(*) AS duplicate_count
FROM projects GROUP BY Project_ID HAVING COUNT(*) > 1;

SELECT Performance_Record_ID, COUNT(*) AS duplicate_count
FROM monthly_performance GROUP BY Performance_Record_ID HAVING COUNT(*) > 1;

SELECT Project_ID, Reporting_Date, COUNT(*) AS duplicate_count
FROM monthly_performance
GROUP BY Project_ID, Reporting_Date
HAVING COUNT(*) > 1;

SELECT Change_Order_ID, COUNT(*) AS duplicate_count
FROM change_orders GROUP BY Change_Order_ID HAVING COUNT(*) > 1;

SELECT RFI_ID, COUNT(*) AS duplicate_count
FROM rfi_log GROUP BY RFI_ID HAVING COUNT(*) > 1;

-- 3. Foreign-key integrity (all queries should return zero rows)
SELECT mp.*
FROM monthly_performance mp
LEFT JOIN projects p ON p.Project_ID = mp.Project_ID
WHERE p.Project_ID IS NULL;

SELECT co.*
FROM change_orders co
LEFT JOIN projects p ON p.Project_ID = co.Project_ID
WHERE p.Project_ID IS NULL;

SELECT r.*
FROM rfi_log r
LEFT JOIN projects p ON p.Project_ID = r.Project_ID
WHERE p.Project_ID IS NULL;

-- 4. Date-sequence validation
SELECT *
FROM projects
WHERE date(Start_Date) >= date(Planned_End_Date);

SELECT *
FROM change_orders
WHERE Approved_Date IS NOT NULL
  AND date(Approved_Date) < date(Submitted_Date);

SELECT *
FROM rfi_log
WHERE Response_Date IS NOT NULL
  AND date(Response_Date) < date(Submitted_Date);

-- 5. Conditional completeness
SELECT *
FROM change_orders
WHERE Change_Status = 'Approved'
  AND (Approved_Date IS NULL OR Approved_Value IS NULL);

SELECT *
FROM rfi_log
WHERE RFI_Status IN ('Answered', 'Closed')
  AND (Response_Date IS NULL OR Response_Days IS NULL);

-- 6. Numeric-range validation
SELECT *
FROM monthly_performance
WHERE Planned_Value < 0 OR Earned_Value < 0 OR Actual_Cost < 0
   OR Percent_Complete NOT BETWEEN 0 AND 100;

SELECT *
FROM projects
WHERE Original_Budget <= 0
   OR Current_Budget < 0
   OR Percent_Complete NOT BETWEEN 0 AND 100;

-- 7. RFI arithmetic consistency
SELECT *
FROM rfi_log
WHERE Response_Date IS NOT NULL
  AND CAST(julianday(Response_Date) - julianday(Submitted_Date) AS INTEGER) <> Response_Days;

-- 8. SQLite engine foreign-key report
PRAGMA foreign_key_check;
