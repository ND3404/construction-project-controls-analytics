# Automation Runbook - Power BI, Tableau, Python, and In Project AI

## What can be automated now?

Yes. The recurring work can be automated, but the appropriate method depends on whether the system remains local or moves to a cloud service.

## Level 1 - Local automation

**Cost:** approximately $0 incremental, excluding existing software and computer use.

Use:

- Windows Task Scheduler
- Python
- a controlled input folder
- CSV outputs
- Power BI Desktop manual refresh

Automate:

1. Validate incoming files
2. Clean or transform data
3. Generate project alerts
4. Generate prediction or scoring outputs
5. Write timestamped logs

Limitation: Power BI Desktop report refresh and publication remain primarily manual. This level is suitable for portfolio development, demonstrations, and testing.

## Level 2 - Power BI cloud automation

Use:

- OneDrive for work or school or SharePoint Online
- Power BI Pro workspace
- scheduled semantic-model refresh
- Power Automate alerts
- optional on-premises data gateway for local/private sources

Recommended sequence:

```text
Source files or database
        ↓
Power Query
        ↓
Published Power BI semantic model
        ↓
Scheduled refresh
        ↓
Refresh history and failure alert
        ↓
Power Automate threshold workflow
        ↓
Email / Teams / action register
```

Power BI supports scheduled and on-demand refresh. Shared capacity supports up to eight scheduled refreshes per day; Premium Per User, Premium, or Fabric capacity supports up to 48 scheduled refreshes per day. Files connected through OneDrive or SharePoint can also synchronize changes, commonly about hourly.

### Suggested automation flows

#### Flow A - Refresh failure

Trigger:
- failed semantic-model refresh or Fabric pipeline failure

Actions:
- notify the data owner;
- include workspace, semantic model, failure time, and refresh-history link;
- create a corrective-action item;
- escalate if not resolved before the next controls meeting.

#### Flow B - Red project exception

Trigger:
- after a successful refresh, or from a Power Automate visual button

Filter:
- Health_Status = Red
- or a project newly crosses a Red threshold

Actions:
- send a concise project summary;
- identify CPI, forecast overrun, delay, contingency use, and primary driver;
- assign the project manager;
- create or update an action-register item.

#### Flow C - RFI escalation

Trigger:
- daily or after refresh

Filter:
- High/Critical RFI is overdue
- or response-time SLA is breached

Actions:
- notify the design manager and discipline owner;
- include RFI identifier, project, age, due date, and responsible party;
- escalate after a defined period.

## Level 3 - Database and model automation

Use:

- Supabase/PostgreSQL reporting views
- a scheduled Python job, Azure Function, GitHub Actions workflow, or Fabric notebook
- prediction output table
- Power BI scheduled refresh
- In Project AI read-only tools

Recommended sequence:

```text
Construction systems
        ↓
Supabase/PostgreSQL or Fabric
        ↓
Scheduled data-engineering job
        ↓
Python model
        ↓
project_risk_predictions
        ↓
Power BI and In Project AI
```

Every prediction record should include:

- Project_ID
- Prediction_Date
- Model_Version
- Cost_Overrun_Probability
- Schedule_Delay_Probability
- Predicted_Delay_Days
- Predicted_Final_Cost
- AI_Risk_Level
- Top_Risk_Factors
- data cutoff or reporting date

## Level 4 - Fabric orchestration

Microsoft Fabric Data Factory pipelines can run:

- on demand;
- on schedules;
- or in response to supported events.

Fabric also provides job scheduling for supported items such as notebooks and can add pipeline-level or activity-level alerts.

Use Fabric when the system needs:

- several connectors;
- recurring pipelines;
- enterprise Microsoft governance;
- larger data volumes;
- model notebooks;
- or coordinated refresh and deployment.

## Tableau automation

Tableau Cloud can schedule extract refreshes for supported cloud-hosted data. Private network or local file sources can use Tableau Bridge for scheduled extract refreshes or live queries. Tableau is a good public-portfolio option for synthetic data, while confidential client deployments require controlled Tableau Cloud/Server security and licensing.

## Recommended choice for this project

### Now

1. Complete the Power BI Desktop report.
2. Store the four analytical CSV files in a controlled OneDrive/SharePoint folder.
3. Publish the PBIX to a Power BI workspace.
4. Configure scheduled refresh.
5. Create refresh-failure and Red-project alerts.
6. Keep Tableau Public only for the synthetic public portfolio.

### Next

1. Move live reporting data to Supabase views.
2. Schedule the Python risk job.
3. Write predictions back to Supabase.
4. Refresh Power BI automatically.
5. Allow In Project AI to retrieve approved metrics and predictions.

### Later

Adopt Fabric only after a pilot demonstrates value and enterprise requirements justify the added cost and complexity.

## Official references

- Power BI data refresh: https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-data
- Power BI scheduled refresh: https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-scheduled-refresh
- Power BI Power Automate visual: https://learn.microsoft.com/en-us/power-bi/create-reports/power-bi-automate-visual
- Power BI pricing: https://www.microsoft.com/en-us/power-platform/products/power-bi/pricing
- Microsoft Fabric pipeline scheduling: https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs
- Microsoft Fabric job scheduler: https://learn.microsoft.com/en-us/fabric/fundamentals/job-scheduler
- Tableau Cloud scheduled refresh: https://help.tableau.com/current/online/en-us/schedule_add.htm
- Tableau Bridge: https://help.tableau.com/current/online/en-us/to_bridge_faq.htm
