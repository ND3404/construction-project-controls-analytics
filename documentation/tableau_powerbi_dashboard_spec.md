# Tableau and Power BI Dashboard Build Specification

## Recommended source

Use:

`analysis/tables/project_performance_analysis.csv`

For monthly trend visuals, also use:

`analysis/tables/monthly_portfolio_trend.csv`

The populated SQLite database is available at:

`data/processed/construction_project_controls_clean.db`

## Page 1 — Executive Portfolio Dashboard

### KPI cards
- Total BAC
- Forecast EAC
- Forecast Overrun %
- Weighted CPI
- Weighted SPI
- Average Schedule Delay Days
- Red Project Count
- Contingency Utilization %

### Visuals
1. Project health distribution — column or donut chart
2. Forecast overrun by project type — horizontal bar chart
3. CPI vs SPI performance matrix — scatterplot
   - X: SPI
   - Y: CPI
   - Detail: Project_ID
   - Size: Original_Budget
   - Color: Health_Status
   - Reference lines: CPI 0.90/0.95 and SPI 0.90/0.95
4. Top-risk projects — ranked table
5. Weighted CPI and SPI monthly trend — line chart

### Filters
- Project Type
- State
- Client Type
- Contract Type
- Delivery Method
- Project Status
- Current Phase
- Health Status

## Page 2 — Operational Drivers

### Visuals
1. Approved change value by cause
2. Change schedule impact by cause
3. Average RFI response days by discipline
4. Late RFI rate by discipline
5. Contingency burn ratio vs forecast overrun scatterplot
6. RFI response days vs schedule delay scatterplot

## Calculated fields

### CPI
`SUM([Earned_Value]) / SUM([Actual_Cost])`

### SPI
`SUM([Earned_Value]) / SUM([Planned_Value])`

### Forecast Overrun %
`([EAC] - [Original_Budget]) / [Original_Budget]`

### Schedule Delay Days
Use the date difference between Forecast_End_Date and Planned_End_Date.

### Health Status
Use the approved Green/Yellow/Red threshold logic from `Definitions_Thresholds` in the Excel workbook.

## Accessibility

- Pair Red/Yellow/Green with visible text labels.
- Use high-contrast headings and readable font sizes.
- Keep currency in en-US format.
- Include tooltips explaining CPI, SPI, EAC, contingency burn, and the synthetic-data disclosure.
- Avoid presenting correlation as causation.
