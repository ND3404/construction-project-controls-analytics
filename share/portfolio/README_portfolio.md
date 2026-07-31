# Construction Project Controls Analytics

## Early Warning Analysis for Cost and Schedule Performance

This portfolio case study demonstrates how project-control data can be consolidated and analyzed to identify construction projects at risk of cost or schedule overruns.

> **Data disclosure:** The dataset is synthetic and does not represent actual clients, contracts, projects, employees, or confidential In Project LLC information.

## Business question

**Which construction projects are most at risk of exceeding their approved budgets or planned completion dates, and what project-control indicators provide the earliest evidence of that risk?**

## Tools

- Excel
- SQL and SQLite
- Earned Value Management
- Data cleaning and relational validation
- Statistical correlation
- Executive dashboard design

## Portfolio results

| KPI | Result |
|---|---:|
| Projects | 75 |
| Portfolio BAC | $5,831,436,600 |
| Forecast EAC | $6,586,989,966 |
| Forecast overrun | 13.0% |
| Weighted CPI | 0.884 |
| Weighted SPI | 0.987 |
| Average forecast delay | 33.7 days |
| Red / Yellow / Green | 50 / 13 / 12 |

## Dashboard

![Executive Dashboard](../assets/executive_dashboard.png)

## Key findings

1. Cost performance was the dominant exposure: weighted CPI was **0.884**.
2. Aggregate EAC was **$6.59B**, approximately **13.0%** above BAC.
3. Contingency burn ratio had a strong association with forecast overrun (**r = 0.901**).
4. Average RFI response time had a moderate association with schedule delay (**r = 0.517**).
5. Calendar completion variance remained essential because SPI can converge at completion.

## Repository outputs

- Cleaned relational data
- SQLite database
- SQL quality and analysis queries
- Formula-driven Excel analysis workbook
- Executive and operational dashboards
- Portfolio-ready HTML case-study pages
- Complete process documentation

## Limitations

The dataset is synthetic, correlations do not prove causation, EAC uses a simplified formula, health thresholds are portfolio assumptions, and small group sizes limit some comparisons.
