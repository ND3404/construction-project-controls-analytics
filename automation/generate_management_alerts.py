#!/usr/bin/env python3
"""Generate an exception file from project_performance_analysis.csv.

This is a rules-based automation starter. It does not retrain a predictive model.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path


def to_float(value: str) -> float:
    return float(value) if value not in ("", None) else 0.0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="../analysis/tables/project_performance_analysis.csv",
        help="Path to the project analysis CSV.",
    )
    parser.add_argument(
        "--output",
        default="output/management_alerts.csv",
        help="Path for the alert output CSV.",
    )
    parser.add_argument("--include-yellow", action="store_true")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    input_path = (script_dir / args.input).resolve()
    output_path = (script_dir / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    alerts = []
    with input_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            status = row.get("Health_Status", "")
            if status == "Red" or (args.include_yellow and status == "Yellow"):
                alerts.append({
                    "Generated_UTC": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "Priority_Rank": row.get("Priority_Rank", ""),
                    "Project_ID": row.get("Project_ID", ""),
                    "Project_Name": row.get("Project_Name", ""),
                    "Health_Status": status,
                    "CPI": row.get("CPI", ""),
                    "SPI": row.get("SPI", ""),
                    "Forecast_Overrun_Pct": row.get("Forecast_Overrun_Pct", ""),
                    "Schedule_Delay_Days": row.get("Schedule_Delay_Days", ""),
                    "Contingency_Utilization_Pct": row.get("Contingency_Utilization_Pct", ""),
                    "Primary_Risk_Driver": row.get("Primary_Risk_Driver", ""),
                    "All_Risk_Triggers": row.get("All_Risk_Triggers", ""),
                    "Recommended_Workflow": (
                        "Immediate executive/project-controls review"
                        if status == "Red"
                        else "Weekly watch-list review"
                    ),
                })

    headers = [
        "Generated_UTC","Priority_Rank","Project_ID","Project_Name","Health_Status",
        "CPI","SPI","Forecast_Overrun_Pct","Schedule_Delay_Days",
        "Contingency_Utilization_Pct","Primary_Risk_Driver","All_Risk_Triggers",
        "Recommended_Workflow",
    ]
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(alerts)

    print(f"Created {len(alerts)} alerts: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
