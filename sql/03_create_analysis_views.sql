-- Construction Project Controls Analytics
-- Analyze Phase: analytical views for SQLite

DROP VIEW IF EXISTS vw_latest_monthly_performance;
CREATE VIEW vw_latest_monthly_performance AS
WITH ranked AS (
    SELECT
        mp.*,
        ROW_NUMBER() OVER (
            PARTITION BY mp.Project_ID
            ORDER BY date(mp.Reporting_Date) DESC
        ) AS rn
    FROM monthly_performance mp
)
SELECT *
FROM ranked
WHERE rn = 1;

DROP VIEW IF EXISTS vw_change_order_summary;
CREATE VIEW vw_change_order_summary AS
SELECT
    Project_ID,
    COUNT(*) AS CO_Count,
    SUM(CASE WHEN Change_Status = 'Approved' THEN 1 ELSE 0 END) AS Approved_CO_Count,
    SUM(CASE WHEN Change_Status = 'Approved' THEN COALESCE(Approved_Value, 0) ELSE 0 END) AS Total_Approved_CO_Value,
    SUM(CASE WHEN Change_Status = 'Pending' THEN COALESCE(Submitted_Value, 0) ELSE 0 END) AS Total_Pending_CO_Value,
    SUM(CASE WHEN Change_Status = 'Approved' THEN Schedule_Impact_Days ELSE 0 END) AS Approved_CO_Schedule_Days,
    AVG(CASE
        WHEN Change_Status = 'Approved' AND Approved_Date IS NOT NULL
        THEN julianday(Approved_Date) - julianday(Submitted_Date)
    END) AS Avg_CO_Approval_Days
FROM change_orders
GROUP BY Project_ID;

DROP VIEW IF EXISTS vw_rfi_summary;
CREATE VIEW vw_rfi_summary AS
SELECT
    Project_ID,
    COUNT(*) AS RFI_Count,
    SUM(CASE WHEN RFI_Status = 'Open' THEN 1 ELSE 0 END) AS Open_RFI_Total,
    AVG(Response_Days) AS Avg_RFI_Response_Days,
    SUM(CASE
        WHEN Response_Date IS NOT NULL
         AND date(Response_Date) > date(Required_Response_Date)
        THEN 1 ELSE 0 END) AS Late_RFI_Count,
    SUM(CASE WHEN Cost_Impact > 0 OR Schedule_Impact_Days > 0 THEN 1 ELSE 0 END) AS Impacted_RFI_Count,
    SUM(Cost_Impact) AS Total_RFI_Cost_Impact,
    SUM(Schedule_Impact_Days) AS Total_RFI_Schedule_Days
FROM rfi_log
GROUP BY Project_ID;

DROP VIEW IF EXISTS vw_project_performance_analysis;
CREATE VIEW vw_project_performance_analysis AS
SELECT
    p.Project_ID,
    p.Project_Name,
    p.Project_Type,
    p.City,
    p.State,
    p.Client_Type,
    p.Contract_Type,
    p.Delivery_Method,
    p.Project_Manager_ID,
    p.Project_Status,
    p.Current_Phase,
    l.Reporting_Date AS Latest_Reporting_Date,
    p.Original_Budget,
    p.Current_Budget,
    p.Original_Contingency,
    l.Planned_Value,
    l.Earned_Value,
    l.Actual_Cost,
    l.Committed_Cost,
    p.Percent_Complete,
    p.Planned_End_Date,
    p.Forecast_End_Date,
    l.Contingency_Used,
    l.Open_RFI_Count AS Latest_Open_RFI_Count,
    COALESCE(co.CO_Count, 0) AS CO_Count,
    COALESCE(co.Approved_CO_Count, 0) AS Approved_CO_Count,
    COALESCE(co.Total_Approved_CO_Value, 0) AS Total_Approved_CO_Value,
    COALESCE(co.Total_Pending_CO_Value, 0) AS Total_Pending_CO_Value,
    COALESCE(co.Approved_CO_Schedule_Days, 0) AS Approved_CO_Schedule_Days,
    co.Avg_CO_Approval_Days,
    COALESCE(r.RFI_Count, 0) AS RFI_Count,
    COALESCE(r.Open_RFI_Total, 0) AS Open_RFI_Total,
    r.Avg_RFI_Response_Days,
    COALESCE(r.Late_RFI_Count, 0) AS Late_RFI_Count,
    COALESCE(r.Impacted_RFI_Count, 0) AS Impacted_RFI_Count,
    COALESCE(r.Total_RFI_Cost_Impact, 0) AS Total_RFI_Cost_Impact,
    COALESCE(r.Total_RFI_Schedule_Days, 0) AS Total_RFI_Schedule_Days,

    CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0) AS CPI,
    CAST(l.Earned_Value AS REAL) / NULLIF(l.Planned_Value, 0) AS SPI,
    l.Earned_Value - l.Actual_Cost AS Cost_Variance,
    l.Earned_Value - l.Planned_Value AS Schedule_Variance,
    p.Original_Budget /
        NULLIF(CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0), 0) AS EAC,
    (
        p.Original_Budget /
        NULLIF(CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0), 0)
    ) - l.Actual_Cost AS ETC,
    p.Original_Budget - (
        p.Original_Budget /
        NULLIF(CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0), 0)
    ) AS VAC,
    (
        (
            p.Original_Budget /
            NULLIF(CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0), 0)
        ) - p.Original_Budget
    ) / NULLIF(p.Original_Budget, 0) AS Forecast_Overrun_Pct,
    CAST(p.Current_Budget - p.Original_Budget AS REAL) /
        NULLIF(p.Original_Budget, 0) AS Cost_Growth_Pct,
    CAST(julianday(p.Forecast_End_Date) - julianday(p.Planned_End_Date) AS INTEGER)
        AS Schedule_Delay_Days,
    CAST(COALESCE(co.Total_Approved_CO_Value, 0) AS REAL) /
        NULLIF(p.Original_Budget, 0) AS Approved_CO_Pct,
    CAST(COALESCE(co.Total_Pending_CO_Value, 0) AS REAL) /
        NULLIF(p.Original_Budget, 0) AS Pending_CO_Pct,
    CAST(l.Contingency_Used AS REAL) /
        NULLIF(p.Original_Contingency, 0) AS Contingency_Utilization_Pct,
    (
        CAST(l.Contingency_Used AS REAL) /
        NULLIF(p.Original_Contingency, 0)
    ) / NULLIF(p.Percent_Complete / 100.0, 0) AS Contingency_Burn_Ratio,
    CAST(COALESCE(r.Late_RFI_Count, 0) AS REAL) /
        NULLIF(COALESCE(r.RFI_Count, 0), 0) AS Late_RFI_Rate,

    CASE
        WHEN (
            CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0) < 0.90
            OR CAST(l.Earned_Value AS REAL) / NULLIF(l.Planned_Value, 0) < 0.90
            OR (
                (
                    p.Original_Budget /
                    NULLIF(CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0), 0)
                ) - p.Original_Budget
            ) / NULLIF(p.Original_Budget, 0) > 0.10
            OR julianday(p.Forecast_End_Date) - julianday(p.Planned_End_Date) > 30
            OR CAST(l.Contingency_Used AS REAL) /
                NULLIF(p.Original_Contingency, 0) > 0.90
            OR (
                CAST(l.Contingency_Used AS REAL) /
                NULLIF(p.Original_Contingency, 0)
            ) / NULLIF(p.Percent_Complete / 100.0, 0) > 1.50
        ) THEN 'Red'
        WHEN (
            CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0) < 0.95
            OR CAST(l.Earned_Value AS REAL) / NULLIF(l.Planned_Value, 0) < 0.95
            OR (
                (
                    p.Original_Budget /
                    NULLIF(CAST(l.Earned_Value AS REAL) / NULLIF(l.Actual_Cost, 0), 0)
                ) - p.Original_Budget
            ) / NULLIF(p.Original_Budget, 0) > 0.05
            OR julianday(p.Forecast_End_Date) - julianday(p.Planned_End_Date) > 15
            OR CAST(l.Contingency_Used AS REAL) /
                NULLIF(p.Original_Contingency, 0) > 0.75
            OR (
                CAST(l.Contingency_Used AS REAL) /
                NULLIF(p.Original_Contingency, 0)
            ) / NULLIF(p.Percent_Complete / 100.0, 0) > 1.20
        ) THEN 'Yellow'
        ELSE 'Green'
    END AS Health_Status
FROM projects p
JOIN vw_latest_monthly_performance l
  ON l.Project_ID = p.Project_ID
LEFT JOIN vw_change_order_summary co
  ON co.Project_ID = p.Project_ID
LEFT JOIN vw_rfi_summary r
  ON r.Project_ID = p.Project_ID;
