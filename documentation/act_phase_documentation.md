# Act Phase - Construction Project Controls Analytics

## Objective

The Act phase converts the approved analytical findings into a practical management response, governance framework, automation roadmap, and implementation sequence.

The recommended decision is to approve a **90-day Project Controls Recovery and Automation Program** with five coordinated workstreams:

1. Immediate intervention on the highest-risk projects
2. Cost, schedule, contingency, change, and RFI control improvements
3. Forecast and portfolio-governance standardization
4. Power BI and workflow automation
5. Predictive analytics and In Project AI integration

## Decision context

The synthetic portfolio contains:

- 75 projects
- $5,831,436,600 total BAC
- $6,586,989,966 forecast EAC
- $755,553,366 unfavorable forecast variance
- 13.0% forecast overrun
- weighted CPI of 0.884
- weighted SPI of 0.987
- 33.7 average forecast-delay days
- 50 Red projects
- 13 Yellow projects
- 12 Green projects

These results describe a synthetic demonstration portfolio and are not construction-industry benchmarks.

## Management recommendations

### 1. Intervene first on the 10 highest-priority projects

The first response should be a focused exception-management process rather than treating all 75 projects equally. Each top-10 project should receive:

- an accountable executive and project owner;
- an independently reviewed EAC;
- a critical-path and constraint review;
- a contingency drawdown review;
- a change-order exposure review;
- an RFI aging review;
- and a dated recovery or mitigation plan.

### 2. Establish cost-recovery reviews

The portfolio weighted CPI of 0.884 indicates material cost inefficiency. For the highest-risk projects, management should validate:

- remaining quantities and productivity;
- committed costs and uncommitted scope;
- accruals and invoices;
- procurement and buyout exposure;
- subcontractor performance;
- remaining contingency;
- and the assumptions supporting ETC and EAC.

### 3. Pair SPI with calendar-based schedule controls

Weighted SPI is 0.987, while average forecast delay is 33.7 days. Management should therefore monitor:

- forecast completion-date variance;
- critical and near-critical paths;
- milestone slippage;
- constraints and procurement;
- recovery logic;
- and 6-week look-ahead reliability.

SPI should not be used as the only schedule indicator.

### 4. Treat contingency burn as a mandatory early-warning measure

The Analyze phase found that contingency burn ratio had the strongest tested association with forecast overrun. Management should require every drawdown to reference:

- the originating risk or approved change;
- the approving authority;
- the amount used;
- remaining contingency;
- physical progress;
- and the updated burn ratio.

### 5. Introduce an RFI response-time service level

The average RFI response time is 14.6 days, and approximately 75.2% of answered RFIs missed their required response date. A proposed initial operating target is:

- average response time of 10 days or less;
- at least 90% on-time response for High and Critical RFIs;
- daily escalation of overdue critical RFIs;
- and discipline-level ownership for recurring delays.

### 6. Strengthen change governance

The portfolio includes $151,618,700 in approved changes and $30,891,200 in pending exposure. The first control focus should be:

- owner-directed changes;
- design errors or omissions;
- unforeseen conditions;
- approval aging;
- schedule impact;
- and timely incorporation into budget and forecast.

### 7. Standardize forecast certification

Every monthly forecast should identify:

- current BAC and authorized budget;
- actual cost and commitments;
- ETC and EAC;
- planned and forecast completion dates;
- contingency balance and burn;
- approved and pending changes;
- major assumptions;
- and reason codes for material changes.

### 8. Automate the data-to-decision workflow

The immediate automation target is:

```text
Governed source files or database
        ↓
Power Query transformation
        ↓
Power BI semantic model
        ↓
Scheduled refresh
        ↓
Automated refresh and threshold alerts
        ↓
Project-controls action register
        ↓
In Project AI explanation layer
```

Formal recommendations, owners, dates, and success measures are contained in the Act workbook.

## 30/60/90-day roadmap

### First 30 days - Control and recover

- Review top-10 projects
- Revalidate EAC and schedule recovery plans
- Implement contingency controls
- Run the RFI closure sprint
- Establish weekly change triage
- Introduce forecast certification
- Finish and validate the Power BI report

### Days 31-60 - Automate and govern

- Publish Power BI to a controlled workspace
- Configure scheduled refresh
- Implement refresh-failure alerts
- Implement Red-project and overdue-RFI alerts
- Create read-only reporting views
- Document refresh ownership, credentials, and recovery procedures

### Days 61-90 - Add predictive and AI capabilities

- Create a versioned Python prediction or rules-based risk model
- Write predictions to a governed table
- Connect approved metrics to In Project AI
- Test answer traceability and access controls
- Run a pilot
- Make a Go / Revise / Stop decision on Fabric and embedded analytics

## Implementation principles

1. Preserve source data and transformation history.
2. Do not automate unsupported assumptions.
3. Keep numerical metrics in governed tables, not in free-form prompts.
4. Separate observed values, forecasts, predictions, and recommendations.
5. Require organization and project authorization on every data request.
6. Maintain refresh, model, and agent audit logs.
7. Scale the architecture only after a working pilot demonstrates value.

## Proposed success measures

The proposed measures are operating targets, not achieved project results:

- 100% top-10 intervention ownership within 3 business days
- 100% weekly review coverage for Red projects
- CPI improvement of at least 0.02 over 90 days
- average forecast-delay reduction of at least 10 days over 90 days
- 100% contingency drawdown traceability
- 90% or better on-time High/Critical RFI response
- 100% approved-change incorporation within 5 business days
- 98% or better Power BI refresh success
- 100% source and reporting-date traceability for AI numerical answers
- zero cross-client data leakage

## Limitations

- The data is synthetic.
- Recommendations demonstrate how management could respond; they are not advice for an actual contract or project.
- Portfolio targets require validation against actual client processes and contractual requirements.
- Predictive results require model testing and monitoring before operational use.
- Power BI, Tableau, Fabric, and AI licensing or service availability may change.

## Capstone-ready Act summary

During the Act phase, I converted the validated analytical findings into a 90-day management and automation program. The plan prioritizes the ten highest-risk projects, requires independent EAC and schedule-recovery reviews, establishes contingency and change-control governance, and introduces an RFI response-time service level. I also designed an automation path that moves governed source data through Power Query and Power BI scheduled refresh into exception alerts, predictive analytics, and an In Project AI explanation layer. The action register assigns owners, dates, deliverables, proposed success measures, and review cadence. Because the dataset is synthetic, the recommendations demonstrate a repeatable decision-support framework rather than claiming actual operational improvement.
