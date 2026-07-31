# Analyze Phase — Construction Project Controls Analytics

## Objective

The Analyze phase transformed the cleaned relational data into project-control metrics, portfolio comparisons, trend analyses, and evidence-based findings aligned with the business task:

> Which construction projects are most at risk of exceeding their approved budgets or planned completion dates, and what project-control indicators provide the earliest evidence of that risk?

## Analytical unit

The principal project-level analysis uses the latest monthly performance record for each of the 75 projects. Change-order and RFI records were aggregated by `Project_ID` and joined to the latest project-performance record.

Monthly portfolio trends use all 1,743 monthly performance records.

## Metrics calculated

- Cost Performance Index (CPI)
- Schedule Performance Index (SPI)
- Cost Variance (CV)
- Schedule Variance (SV)
- Estimate at Completion (EAC)
- Estimate to Complete (ETC)
- Variance at Completion (VAC)
- Forecast cost overrun percentage
- Cost growth percentage
- Forecast schedule delay in days
- Approved and pending change-order exposure
- Contingency utilization and contingency burn ratio
- RFI response time, late-response rate, and impact rates
- Project health classification

## Project-health logic

A project is classified as **Red** if any Red threshold is breached:

- CPI < 0.90
- SPI < 0.90
- Forecast overrun > 10%
- Forecast delay > 30 days
- Contingency utilization > 90%
- Contingency burn ratio > 1.50x

If no Red threshold is breached, the project is **Yellow** when any Yellow threshold is breached. Otherwise, it is **Green**.

These thresholds are portfolio assumptions approved during the ASK phase. They are not universal construction standards.

# Portfolio results

| Metric | Result |
|---|---:|
| Projects | 75 |
| Total BAC | $5,831,436,600 |
| Forecast EAC | $6,586,989,966 |
| Net forecast variance | $755,553,366 unfavorable |
| Forecast overrun | 13.0% |
| Weighted CPI | 0.884 |
| Weighted SPI | 0.987 |
| Average forecast delay | 33.7 days |
| Median forecast delay | 38 days |
| Approved change value | $151,618,700 |
| Pending change exposure | $30,891,200 |
| Contingency utilization | 66.2% |
| Red projects | 50 |
| Yellow projects | 13 |
| Green projects | 12 |

## Finding 1 — Cost performance is the portfolio’s dominant exposure

The weighted CPI is **0.884**, meaning the portfolio is earning approximately $0.88 of budgeted value for every $1.00 spent at the latest reporting dates.

The aggregate EAC is **$6.59 billion**, compared with a BAC of **$5.83 billion**. This produces an unfavorable net forecast variance of approximately **$755.6 million**, or **13.0%**.

## Finding 2 — Calendar delay reveals exposure that portfolio SPI can obscure

The weighted SPI is **0.987**, close to 1.00, while the average forecast delay is **33.7 days**.

This is not contradictory. On completed or nearly completed projects, PV and EV can converge at BAC even when the project finished late. The analysis therefore uses both SPI and forecast completion-date variance. Calendar delay is essential for interpreting schedule performance across projects at different stages.

## Finding 3 — The portfolio is heavily concentrated in Red status

Under the approved threshold logic:

- **50 projects (66.7%)** are Red.
- **13 projects (17.3%)** are Yellow.
- **12 projects (16.0%)** are Green.

The synthetic portfolio was designed to include meaningful deterioration and intervention cases. The high Red share should not be interpreted as an industry failure rate.

## Finding 4 — Project type shows meaningful performance variation

**Mixed-Use** has the highest portfolio-weighted forecast overrun at **16.3%** and an average forecast delay of **46.8 days**.

**Heavy Civil & Infrastructure** has the lowest forecast overrun at **9.4%** and an average forecast delay of **8.3 days**.

These are associations within the synthetic portfolio. Project type alone does not establish the cause of performance differences.

## Finding 5 — CMAR performs better in this dataset, but method comparisons require caution

CMAR projects show:

- weighted CPI of **0.910**;
- forecast overrun of **9.6%**;
- average delay of **22.7 days**;
- Red-project rate of **52.9%**.

Integrated Project Delivery shows a forecast overrun of **14.6%**, but the group contains only **5 projects**. The sample is too small for broad conclusions about the delivery method.

## Finding 6 — Contingency burn is the strongest early-warning relationship tested

The contingency burn ratio has a **strong positive association** with forecast cost overrun:

- Pearson r = **0.901**
- R² = **0.812**

Projects consuming contingency faster than physical progress tend to have larger forecast overruns in this dataset. This is an association and does not prove causation, but it is a strong candidate for early-warning monitoring.

## Finding 7 — RFI response time is more informative than RFI volume

Average RFI response days have a **moderate positive association** with schedule delay:

- Pearson r = **0.517**
- R² = **0.267**

By contrast, RFI density per $10 million has a weak association with delay. This suggests that response timeliness may be more analytically useful than raw RFI counts when project sizes differ.

Electrical and Structural RFIs have the longest average response times:

- Electrical: **15.5 days**
- Structural: **15.3 days**

## Finding 8 — Change-order value is associated with forecast overrun

Approved change-order percentage has a **moderate positive association** with forecast overrun:

- Pearson r = **0.400**
- R² = **0.160**

Owner-directed changes account for the largest approved value at **$42,848,100**. Design errors or omissions account for **$31,940,300**, while unforeseen conditions produce the largest approved schedule impact at **700 days**.

### Important definitional relationship

Approved CO % and Cost Growth % have a near-perfect correlation because `Current_Budget` was defined as `Original_Budget + approved change orders`.

That relationship validates the data model but is **not an independent analytical finding** and must not be presented as evidence that change orders caused cost growth.

## Finding 9 — Highest-priority projects

The first three projects in the transparent priority ordering are:

1. **PRJ-075 — Canyon Ridge Transit-Oriented Development**
   - CPI: 0.753
   - Forecast overrun: 32.9%
   - Delay: 73 days
   - Contingency utilization: 107.1%

2. **PRJ-009 — Northstar Housing**
   - CPI: 0.755
   - Forecast overrun: 32.5%
   - Delay: 63 days
   - Contingency utilization: 105.6%

3. **PRJ-046 — Red Rock Residences**
   - CPI: 0.779
   - Forecast overrun: 28.4%
   - Delay: 84 days
   - Contingency utilization: 107.1%

The priority order is based on health status, number of critical threshold breaches, forecast overrun, and schedule delay. It is transparent and does not use an unexplained proprietary score.

# Analytical limitations

1. The dataset is synthetic and cannot establish industry benchmarks.
2. Correlation does not prove causation.
3. EAC uses the simplified formula `BAC / CPI`.
4. SPI can lose interpretive power at or after planned completion.
5. Project complexity is not fully observable.
6. Some group comparisons have small sample sizes.
7. Change-order causes and RFI disciplines are simplified categories.
8. Health thresholds are portfolio assumptions.
9. The analysis uses the latest record for cross-sectional project comparison.
10. Additional time-series modeling could evaluate when each warning indicator first became material.

# Outputs

- Formula-driven Excel analysis workbook
- Project-level analytical CSV
- Portfolio and segmentation summary CSVs
- Monthly trend CSV
- Correlation summary
- Top-risk project table
- SQLite analytical views
- Reusable SQL business queries

# Capstone-ready Analyze summary

During the Analyze phase, I joined the latest monthly performance record for each of 75 projects with aggregated change-order and RFI information. I calculated CPI, SPI, CV, SV, EAC, ETC, VAC, forecast cost overrun, schedule delay, contingency utilization, contingency burn, change exposure, and RFI performance. The portfolio had a weighted CPI of 0.884 and a forecast EAC of $6.59 billion, which was 13.0% above the $5.83 billion BAC. Fifty projects met at least one Red threshold. The strongest tested early-warning relationship was between contingency burn ratio and forecast overrun (r = 0.901), while average RFI response time showed a moderate positive association with schedule delay (r = 0.517). I treated these as associations rather than causal proof and documented the synthetic data, assumptions, group-size limitations, and definitional relationships.
