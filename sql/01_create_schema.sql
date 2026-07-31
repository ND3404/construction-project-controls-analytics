-- Construction Project Controls Analytics
-- Process Phase: SQLite schema for the cleaned relational dataset
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects (
    Project_ID TEXT PRIMARY KEY,
    Project_Name TEXT NOT NULL,
    Project_Type TEXT NOT NULL,
    City TEXT NOT NULL,
    State TEXT NOT NULL,
    Client_Type TEXT NOT NULL,
    Contract_Type TEXT NOT NULL,
    Delivery_Method TEXT NOT NULL,
    Project_Manager_ID TEXT NOT NULL,
    Original_Budget INTEGER NOT NULL CHECK (Original_Budget > 0),
    Current_Budget INTEGER NOT NULL CHECK (Current_Budget >= 0),
    Original_Contingency INTEGER NOT NULL CHECK (Original_Contingency >= 0),
    Start_Date TEXT NOT NULL,
    Planned_End_Date TEXT NOT NULL,
    Forecast_End_Date TEXT NOT NULL,
    Project_Status TEXT NOT NULL,
    Current_Phase TEXT NOT NULL,
    Percent_Complete REAL NOT NULL CHECK (Percent_Complete BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS monthly_performance (
    Performance_Record_ID TEXT PRIMARY KEY,
    Project_ID TEXT NOT NULL,
    Reporting_Date TEXT NOT NULL,
    Planned_Value INTEGER NOT NULL CHECK (Planned_Value >= 0),
    Earned_Value INTEGER NOT NULL CHECK (Earned_Value >= 0),
    Actual_Cost INTEGER NOT NULL CHECK (Actual_Cost >= 0),
    Percent_Complete REAL NOT NULL CHECK (Percent_Complete BETWEEN 0 AND 100),
    Committed_Cost INTEGER NOT NULL CHECK (Committed_Cost >= 0),
    Contingency_Used INTEGER NOT NULL CHECK (Contingency_Used >= 0),
    Forecast_End_Date TEXT NOT NULL,
    Open_RFI_Count INTEGER NOT NULL CHECK (Open_RFI_Count >= 0),
    Pending_CO_Value INTEGER NOT NULL CHECK (Pending_CO_Value >= 0),
    Approved_CO_Value INTEGER NOT NULL CHECK (Approved_CO_Value >= 0),
    FOREIGN KEY (Project_ID) REFERENCES projects(Project_ID),
    UNIQUE (Project_ID, Reporting_Date)
);

CREATE TABLE IF NOT EXISTS change_orders (
    Change_Order_ID TEXT PRIMARY KEY,
    Project_ID TEXT NOT NULL,
    Change_Title TEXT NOT NULL,
    Change_Category TEXT NOT NULL,
    Responsible_Party TEXT NOT NULL,
    Submitted_Date TEXT NOT NULL,
    Approved_Date TEXT,
    Submitted_Value INTEGER NOT NULL CHECK (Submitted_Value >= 0),
    Approved_Value INTEGER CHECK (Approved_Value >= 0),
    Schedule_Impact_Days INTEGER NOT NULL CHECK (Schedule_Impact_Days >= 0),
    Change_Status TEXT NOT NULL,
    Discipline TEXT NOT NULL,
    FOREIGN KEY (Project_ID) REFERENCES projects(Project_ID)
);

CREATE TABLE IF NOT EXISTS rfi_log (
    RFI_ID TEXT PRIMARY KEY,
    Project_ID TEXT NOT NULL,
    RFI_Title TEXT NOT NULL,
    Discipline TEXT NOT NULL,
    Submitted_Date TEXT NOT NULL,
    Required_Response_Date TEXT NOT NULL,
    Response_Date TEXT,
    RFI_Status TEXT NOT NULL,
    Response_Days INTEGER CHECK (Response_Days >= 0),
    Responsible_Party TEXT NOT NULL,
    Cost_Impact INTEGER NOT NULL CHECK (Cost_Impact >= 0),
    Schedule_Impact_Days INTEGER NOT NULL CHECK (Schedule_Impact_Days >= 0),
    Priority TEXT NOT NULL,
    FOREIGN KEY (Project_ID) REFERENCES projects(Project_ID)
);

CREATE INDEX IF NOT EXISTS idx_monthly_project_date
    ON monthly_performance(Project_ID, Reporting_Date);
CREATE INDEX IF NOT EXISTS idx_change_project
    ON change_orders(Project_ID);
CREATE INDEX IF NOT EXISTS idx_change_category
    ON change_orders(Change_Category);
CREATE INDEX IF NOT EXISTS idx_rfi_project
    ON rfi_log(Project_ID);
CREATE INDEX IF NOT EXISTS idx_rfi_status
    ON rfi_log(RFI_Status);
