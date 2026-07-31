# Loading the Cleaned CSV Files into SQL

A populated SQLite database is already included at:

`data/processed/construction_project_controls_clean.db`

The following table counts were validated:

- projects: 75
- monthly_performance: 1,743
- change_orders: 553
- rfi_log: 1,514

For another database platform, use `sql/01_create_schema.sql`, import the four cleaned CSV files, and then run `sql/02_data_quality_checks.sql`.

## Recommended import order

1. `projects_clean.csv`
2. `monthly_performance_clean.csv`
3. `change_orders_clean.csv`
4. `rfi_log_clean.csv`

The parent `projects` table must be loaded first because the other tables use `Project_ID` as a foreign key.
