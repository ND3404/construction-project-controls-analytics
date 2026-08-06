# START HERE - Construction Project Controls Analytics Case Study

## Project status

All six Google Data Analytics phases are complete:

- Ask
- Prepare
- Process
- Analyze
- Share
- Act

## Recommended opening order

1. `reports/Construction_Project_Controls_Analytics_Case_Study.pdf`
2. `act/construction_project_controls_act_plan.xlsx`
3. `share/construction_project_controls_share_dashboard.xlsx`
4. `analysis/excel/construction_project_controls_analysis.xlsx`
5. `automation/README.md`

## Power BI source files

Use the analytical CSV files in:

`analysis/tables/`

The primary table is:

`analysis/tables/project_performance_analysis.csv`

Supporting tables include:

- `monthly_portfolio_trend.csv`
- `change_category_summary.csv`
- `rfi_discipline_summary.csv`

## Local automation starter

From PowerShell:

```powershell
cd "C:\Users\narci\projects\Construction Project Controls Analytics case study\automation"
.\run_analytics_pipeline.ps1
```

To include Yellow projects in the management-alert output:

```powershell
.\run_analytics_pipeline.ps1 -IncludeYellow
```

The starter writes alerts to:

`automation/output/management_alerts.csv`

It also creates timestamped logs in:

`automation/logs/`

## Cloud automation path

1. Finish the Power BI Desktop report.
2. Move source files to controlled OneDrive/SharePoint storage or a governed database.
3. Publish the PBIX to a Power BI workspace.
4. Configure scheduled refresh.
5. Add refresh-failure and Red-project workflows.
6. Later connect Supabase, a scheduled Python model, and In Project AI.
7. Adopt Microsoft Fabric only when a pilot and client requirements justify it.

## Disclosure

All portfolio records are synthetic and must always be represented as educational and demonstration data.
