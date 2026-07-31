-- Analyze Phase: business and project-control queries

-- 1. Portfolio summary
SELECT
    COUNT(*) AS Project_Count,
    SUM(Original_Budget) AS Total_BAC,
    SUM(EAC) AS Total_EAC,
    SUM(EAC - Original_Budget) AS Net_Forecast_Variance,
    SUM(Earned_Value) / NULLIF(SUM(Actual_Cost), 0) AS Weighted_CPI,
    SUM(Earned_Value) / NULLIF(SUM(Planned_Value), 0) AS Weighted_SPI,
    AVG(Schedule_Delay_Days) AS Average_Delay_Days,
    SUM(CASE WHEN Health_Status = 'Red' THEN 1 ELSE 0 END) AS Red_Projects,
    SUM(CASE WHEN Health_Status = 'Yellow' THEN 1 ELSE 0 END) AS Yellow_Projects,
    SUM(CASE WHEN Health_Status = 'Green' THEN 1 ELSE 0 END) AS Green_Projects
FROM vw_project_performance_analysis;

-- 2. Projects requiring management attention
SELECT
    Project_ID,
    Project_Name,
    Project_Type,
    CPI,
    SPI,
    Forecast_Overrun_Pct,
    Schedule_Delay_Days,
    Contingency_Utilization_Pct,
    Health_Status
FROM vw_project_performance_analysis
ORDER BY
    CASE Health_Status WHEN 'Red' THEN 1 WHEN 'Yellow' THEN 2 ELSE 3 END,
    Forecast_Overrun_Pct DESC,
    Schedule_Delay_Days DESC;

-- 3. Performance by project type
SELECT
    Project_Type,
    COUNT(*) AS Project_Count,
    SUM(Original_Budget) AS Total_BAC,
    SUM(Earned_Value) / NULLIF(SUM(Actual_Cost), 0) AS Weighted_CPI,
    SUM(Earned_Value) / NULLIF(SUM(Planned_Value), 0) AS Weighted_SPI,
    (SUM(EAC) - SUM(Original_Budget)) / NULLIF(SUM(Original_Budget), 0)
        AS Forecast_Overrun_Pct,
    AVG(Schedule_Delay_Days) AS Average_Delay_Days,
    AVG(Approved_CO_Pct) AS Average_Approved_CO_Pct,
    AVG(Avg_RFI_Response_Days) AS Average_RFI_Response_Days,
    AVG(CASE WHEN Health_Status = 'Red' THEN 1.0 ELSE 0.0 END) AS Red_Project_Rate
FROM vw_project_performance_analysis
GROUP BY Project_Type
ORDER BY Forecast_Overrun_Pct DESC;

-- 4. Performance by delivery method
SELECT
    Delivery_Method,
    COUNT(*) AS Project_Count,
    SUM(Earned_Value) / NULLIF(SUM(Actual_Cost), 0) AS Weighted_CPI,
    SUM(Earned_Value) / NULLIF(SUM(Planned_Value), 0) AS Weighted_SPI,
    (SUM(EAC) - SUM(Original_Budget)) / NULLIF(SUM(Original_Budget), 0)
        AS Forecast_Overrun_Pct,
    AVG(Schedule_Delay_Days) AS Average_Delay_Days,
    AVG(CASE WHEN Health_Status = 'Red' THEN 1.0 ELSE 0.0 END) AS Red_Project_Rate
FROM vw_project_performance_analysis
GROUP BY Delivery_Method
ORDER BY Forecast_Overrun_Pct DESC;

-- 5. Change-order causes
SELECT
    Change_Category,
    COUNT(*) AS Change_Count,
    SUM(CASE WHEN Change_Status = 'Approved' THEN Approved_Value ELSE 0 END)
        AS Approved_Value,
    SUM(CASE WHEN Change_Status = 'Approved' THEN Schedule_Impact_Days ELSE 0 END)
        AS Approved_Schedule_Impact_Days,
    AVG(CASE
        WHEN Change_Status = 'Approved' AND Approved_Date IS NOT NULL
        THEN julianday(Approved_Date) - julianday(Submitted_Date)
    END) AS Avg_Approval_Days
FROM change_orders
GROUP BY Change_Category
ORDER BY Approved_Value DESC;

-- 6. RFI performance by discipline
SELECT
    Discipline,
    COUNT(*) AS RFI_Count,
    AVG(Response_Days) AS Avg_Response_Days,
    AVG(CASE
        WHEN Response_Date IS NOT NULL
         AND date(Response_Date) > date(Required_Response_Date)
        THEN 1.0 ELSE 0.0 END) AS Late_RFI_Rate,
    SUM(Cost_Impact) AS Total_Cost_Impact,
    SUM(Schedule_Impact_Days) AS Total_Schedule_Impact_Days
FROM rfi_log
GROUP BY Discipline
ORDER BY Avg_Response_Days DESC;

-- 7. Portfolio monthly trend
SELECT
    Reporting_Date,
    COUNT(DISTINCT Project_ID) AS Reporting_Project_Count,
    SUM(Earned_Value) / NULLIF(SUM(Actual_Cost), 0) AS Weighted_CPI,
    SUM(Earned_Value) / NULLIF(SUM(Planned_Value), 0) AS Weighted_SPI,
    SUM(Contingency_Used) AS Total_Contingency_Used,
    SUM(Approved_CO_Value) AS Total_Approved_CO_Value,
    SUM(Pending_CO_Value) AS Total_Pending_CO_Value
FROM monthly_performance
GROUP BY Reporting_Date
ORDER BY date(Reporting_Date);

-- Important analytical note:
-- Cost_Growth_Pct is arithmetically linked to Approved_CO_Pct because Current_Budget
-- was defined as Original_Budget plus approved change orders. Their near-perfect
-- correlation is a validation of the data model, not an independent causal finding.
