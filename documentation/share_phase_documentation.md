# Share Phase — Construction Project Controls Analytics

## Objective

The Share phase converted validated analytical results into a clear executive communication package for:

- executive leadership;
- project-controls management;
- project managers;
- cost managers;
- schedulers;
- prospective employers reviewing a personal data-analytics portfolio;
- and prospective In Project LLC clients evaluating construction-analytics capability.

The communication objective was to answer three questions quickly:

1. What is the overall portfolio exposure?
2. Which projects require management attention?
3. Which operational patterns deserve deeper review?

Formal management recommendations and implementation priorities remain part of the ACT phase.

## Primary communication product

### Construction Project Controls Executive Dashboard

The executive dashboard presents the analytical story in this order:

1. Portfolio BAC and forecast EAC
2. Forecast overrun and Red-project count
3. Weighted CPI and SPI
4. Average forecast delay and contingency utilization
5. Portfolio health distribution
6. Forecast overrun by project type
7. Top 10 projects requiring attention
8. Monthly CPI and SPI trend
9. Concise executive interpretation
10. Data and causality disclosure

## Secondary communication product

### Operational Insights Dashboard

The operational view presents:

- approved change value by cause;
- average RFI response time by discipline;
- relationship testing;
- correlation strength and intended management use;
- diagnostic messages;
- and communication/accessibility notes.

## Visual selection rationale

| Visual | Purpose |
|---|---|
| KPI cards | Communicate portfolio scale and exposure immediately |
| Health distribution chart | Show the concentration of Red, Yellow, and Green projects |
| Forecast overrun by project type | Compare normalized portfolio performance across sectors |
| Top-risk table | Support project-level management prioritization |
| CPI/SPI trend | Show whether portfolio efficiency is improving or deteriorating |
| Change-value bar chart | Identify major sources of approved cost growth |
| RFI response-time chart | Compare workflow performance by discipline |
| Correlation table | Show strength, direction, use, and limitations of tested relationships |

## Key messages communicated

- Portfolio BAC: **$5,831,436,600**
- Forecast EAC: **$6,586,989,966**
- Forecast overrun: **13.0%**
- Weighted CPI: **0.884**
- Weighted SPI: **0.987**
- Average forecast delay: **33.7 days**
- Health distribution: **50 Red, 13 Yellow, 12 Green**
- Strongest tested warning relationship: contingency burn ratio vs forecast overrun, **r = 0.901**
- RFI response time vs schedule delay: **r = 0.517**

## Executive narrative

The synthetic portfolio shows significant cost exposure. Weighted CPI is below 0.90, and forecast EAC is approximately 13.0% above BAC. Although weighted SPI is close to 1.00, average forecast delay remains material, demonstrating why calendar completion variance must be evaluated alongside earned-value schedule indicators.

Contingency burn is the strongest early-warning relationship tested. Projects consuming contingency faster than physical progress tend to show larger forecast overruns. Average RFI response time also has a meaningful positive association with schedule delay, while raw RFI density has little explanatory value in this portfolio.

## Accessibility and ethical communication

The visual package uses:

- high-contrast navy and blue headings;
- text labels in addition to status colors;
- readable U.S. currency and percentage formats;
- limited dependence on color alone;
- concise annotations next to visuals;
- explicit synthetic-data disclosure;
- and repeated reminders that correlation does not prove causation.

Red, Yellow, and Green classifications are portfolio assumptions established in the ASK phase. They are not presented as universal industry standards.

## Communication channels

### Personal portfolio

The personal portfolio HTML page emphasizes:

- the business problem;
- analytical workflow;
- skills and tools;
- dashboard outputs;
- findings;
- limitations;
- and downloadable evidence.

### In Project LLC

The company-facing HTML page emphasizes:

- project-controls analytics capability;
- executive reporting;
- cost and schedule performance;
- change and RFI diagnostics;
- portfolio risk classification;
- and data-driven construction services.

### GitHub

The GitHub-ready summary provides:

- business question;
- methodology;
- dashboard image;
- results;
- tools;
- output structure;
- and limitations.

### Tableau or Power BI

A dashboard build specification identifies the prepared data sources, visuals, filters, calculated fields, and accessibility requirements for a future interactive implementation.

## Share-phase deliverables

- `share/construction_project_controls_share_dashboard.xlsx`
- `share/assets/executive_dashboard.png`
- `share/assets/operational_insights.png`
- `share/portfolio/personal_portfolio_case_study.html`
- `share/portfolio/in_project_case_study.html`
- `share/portfolio/README_portfolio.md`
- `documentation/tableau_powerbi_dashboard_spec.md`
- `documentation/share_phase_documentation.md`
- `documentation/share_manifest.json`

## Capstone-ready Share summary

During the Share phase, I translated the analytical results into an executive project-controls dashboard and an operational diagnostic dashboard. I structured the communication around portfolio exposure, projects requiring management attention, contributing operational patterns, and analytical limitations. The dashboard highlighted a $5.83 billion portfolio BAC, a $6.59 billion forecast EAC, a 13.0% forecast overrun, weighted CPI of 0.884, and 50 Red projects. I used KPI cards, bar charts, a monthly performance trend, a ranked project table, and an annotated correlation table. I paired status colors with text, used readable currency and percentage formats, disclosed that the data was synthetic, and avoided presenting correlations as causal proof. I also created personal-portfolio and company-facing case-study pages and prepared a Tableau/Power BI dashboard specification for future interactive publication.
