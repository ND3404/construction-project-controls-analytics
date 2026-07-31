# Dataset Methodology

## 1. Objective

The dataset was designed to support analysis of construction project cost, schedule, change, RFI, and contingency performance across a fictional U.S. project portfolio.

The primary business question is:

> Which construction projects are most at risk of exceeding their approved budgets or planned completion dates, and what project-control indicators provide the earliest evidence of that risk?

## 2. Data classification and ownership

- Data type: Synthetic educational and demonstration data
- Creator: Narciso M. Dickson / In Project LLC portfolio project
- Intended use: Google Data Analytics capstone, professional portfolio, interview demonstration, and In Project LLC capability demonstration
- Confidentiality: No actual client, employee, contract, address, or project performance data is included
- Currency: U.S. dollars
- Dataset version: 1.0
- Reproducibility seed: 3404

## 3. Portfolio scope

- Intended unique projects: 75
- Reporting period: January 2022 through December 2025
- Project sectors: Residential, Commercial, Institutional, Industrial, Heavy Civil & Infrastructure, and Mixed-Use
- Geographic coverage: Fictional projects assigned to cities in ten western and southern U.S. states
- Contract types: Lump Sum, Guaranteed Maximum Price, Cost Plus, and Unit Price
- Delivery methods: Design-Bid-Build, Design-Build, CMAR, and Integrated Project Delivery

## 4. Relational data model

### Projects
Grain: One row per intended construction project.

### Monthly Performance
Grain: One row per project per reporting month.

### Change Orders
Grain: One row per change order.

### RFI Log
Grain: One row per request for information.

The three child tables connect to the Projects table through `Project_ID`.

## 5. Generation logic

The data was not generated as unrelated random values. Each project received unreported latent risk, complexity, and recovery characteristics that influenced multiple operational variables.

### Cost and schedule
- Planned Value follows a cumulative S-curve across the baseline duration.
- Earned Value follows progress across the forecast duration.
- Actual Cost is generated from Earned Value and a changing cost-efficiency profile.
- Cost efficiency varies by project and can improve or deteriorate over time.
- Forecast completion incorporates project risk, complexity, approved change impacts, RFI response behavior, and controlled random variation.
- Some projects recover after corrective action, while others deteriorate.

### Change orders
- Change-order frequency varies with project scale, complexity, and risk.
- Categories include owner changes, design errors or omissions, unforeseen conditions, coordination issues, regulatory changes, and other common causes.
- Submitted values are scaled to project budget.
- Approved changes include realistic approval durations and schedule impacts.

### RFIs
- RFI frequency varies with project scale, risk, and complexity.
- Response time varies by priority and project conditions.
- A subset of RFIs has cost or schedule impact.
- Recently submitted RFIs may remain open at the portfolio reporting date.

### Contingency
- Contingency consumption increases with progress, risk, and change pressure.
- Some projects consume contingency faster than physical progress, creating an analytical warning indicator.

## 6. Performance relationships

The generated portfolio contains probabilistic—not guaranteed—relationships such as:

- higher change-order exposure may be associated with cost growth;
- longer RFI response times may be associated with schedule pressure;
- high RFI backlog may accompany lower schedule performance;
- higher-risk projects may consume contingency more quickly;
- projects in every category can perform well or poorly.

The dataset does not predetermine that a specific contract type, delivery method, sector, state, or project manager will fail.

## 7. Raw-data quality design

The raw files include a controlled number of realistic issues to support the Process phase. Issue categories include:

- duplicate records;
- inconsistent capitalization and trailing spaces;
- mixed date formats;
- currency symbols or commas in numeric fields;
- percentages stored with percent signs;
- selected missing values;
- invalid parent identifiers;
- inconsistent status or discipline labels;
- illogical date sequences;
- and an isolated numerical outlier.

Some blanks are legitimate. For example, an open RFI may have no response date, and a pending change order may have no approved date or approved value.

Exact issue locations are intentionally omitted so the analyst can perform independent profiling and document the cleaning process.

## 8. Data-integrity expectations

- `Project_ID` should be unique in Projects after cleaning.
- Child-table project identifiers should match the Projects table.
- Monthly data should contain no more than one record per project and reporting month.
- Dates should follow logical sequences.
- Percentage values should remain between 0 and 100.
- Financial values should be numeric and nonnegative.
- Approved changes should have approved dates and values.
- Open RFIs may have blank response dates; answered or closed RFIs should not.

## 9. Limitations

1. The data is synthetic and cannot establish actual construction-industry benchmarks.
2. Earned Value Management practices differ among organizations.
3. RFI count does not fully represent technical complexity.
4. Change orders may be symptoms rather than root causes.
5. External influences such as labor markets, inflation, permitting, weather, and supply chains are simplified.
6. Associations should not be presented as proof of causation.
7. The dataset is designed for decision-support demonstration, not contractual or financial decision-making.

## 10. Ethical use statement

This dataset must always be represented as synthetic. It should not be described as actual In Project LLC client performance or as verified industry research.
