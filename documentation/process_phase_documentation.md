# Process Phase — Construction Project Controls Analytics

## Objective

The Process phase transformed four raw CSV files into a clean, relational, analysis-ready dataset while preserving the original raw data unchanged.

## Tools used

- Python standard library for reproducible parsing and transformation
- Excel audit workbook for the cleaning log and validation evidence
- SQLite for relational storage and SQL validation

## Raw-data profile

| Table | Raw rows | Clean rows |
|---|---:|---:|
| Projects | 77 | 75 |
| Monthly Performance | 1,747 | 1,743 |
| Change Orders | 557 | 553 |
| RFI Log | 1,518 | 1,514 |
| **Total** | **3,899** | **3,885** |

## Cleaning results

- 12 duplicate rows were removed.
- 2 child records with unverifiable Project_ID values were quarantined rather than guessed.
- 16 critical values were repaired using documented, evidence-based rules.
- At least 111 categorical, date, ID, currency, or percentage values were standardized.
- All 22 final validation checks passed.
- The SQLite `PRAGMA foreign_key_check` returned no violations.

## Principal treatments

### Projects
- Removed duplicate Project_ID records.
- Standardized project type, state, dates, currency, and percentage fields.
- Classified missing contract types as `Unknown` instead of inferring a contract type.

### Monthly performance
- Removed duplicate performance records.
- Standardized dates, project identifiers, currency, and percentage fields.
- Reconstructed six missing Actual_Cost values from adjacent cumulative records.
- Corrected one isolated impossible cumulative-cost spike using adjacent project periods.

### Change orders
- Removed duplicates and standardized categories, status values, dates, and currency.
- Used Submitted_Value as a documented proxy for two approved records missing Approved_Value.
- Corrected two impossible approval dates using the median approval cycle for the same change category.
- Quarantined one record with an unmatched Project_ID.

### RFIs
- Removed duplicates and standardized disciplines, statuses, dates, IDs, and response-day values.
- Reconstructed three missing response dates from Submitted_Date plus Response_Days.
- Corrected two response dates that preceded submission.
- Quarantined one record with an unmatched Project_ID.

## Ethical and analytical controls

No unmatched Project_ID was guessed. Rejected records remain available in `data/processed/rejected_records.csv`. Imputations were limited to cases with direct internal evidence or clearly documented portfolio-based rules. The raw files remain unchanged.

## Output

The cleaned dataset consists of:

- `data/cleaned/projects_clean.csv`
- `data/cleaned/monthly_performance_clean.csv`
- `data/cleaned/change_orders_clean.csv`
- `data/cleaned/rfi_log_clean.csv`
- `data/processed/construction_project_controls_clean.db`
- `documentation/data_cleaning_log.xlsx`

## Capstone-ready Process summary

During the Process phase, I profiled 3,899 raw records across four relational tables and standardized data types, categories, dates, identifiers, currency fields, and percentages. I removed 12 duplicate records and quarantined two child records with invalid project relationships rather than making unsupported corrections. I repaired 16 critical values using documented business rules, including cumulative cost interpolation, change-order approval-cycle logic, and RFI response-date reconstruction. The resulting dataset contained 3,885 clean records. I validated primary keys, project relationships, date sequences, required fields, numeric ranges, cumulative measures, and RFI duration calculations. All 22 final validation checks passed, and the cleaned files were loaded into a SQLite database with no foreign-key violations.
