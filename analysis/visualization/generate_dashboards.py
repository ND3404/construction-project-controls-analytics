"""
Construction Project Controls Analytics - dashboard generation.

Builds the two portfolio dashboards in share/assets/excel_screenshots/ from the
analytical CSV outputs in analysis/tables/. These replace the earlier Excel
screen captures so all three portfolio projects share one visual system.

Usage:
    python analysis/visualization/generate_dashboards.py [output_dir]

Data disclosure: all records are synthetic.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inproject_bi import (  # noqa: E402
    Dashboard, STATUS, BRICK, BRICK_2, NAVY_3, GREEN, AMBER, RED, INK, MUTED,
    MONEY, money, hbar, grouped_bar, donut, table_panel,
)

ROOT = Path(__file__).resolve().parents[2]
T = ROOT / "analysis" / "tables"
OUT = (Path(sys.argv[1]) if len(sys.argv) > 1
       else ROOT / "share" / "assets" / "excel_screenshots")

STEEL = "#53616D"


def read(n):
    return pd.read_csv(T / n, encoding="utf-8-sig")


summ = read("portfolio_summary.csv").set_index("Metric")["Value"].astype(float)
perf = read("project_performance_analysis.csv")
top10 = read("top_10_risk_projects.csv")
ptype = read("project_type_summary.csv")
deliv = read("delivery_method_summary.csv")
cat = read("change_category_summary.csv")
disc = read("rfi_discipline_summary.csv")
corr = read("correlation_summary.csv")
trend = read("monthly_portfolio_trend.csv")

BANDS = ["Red", "Yellow", "Green"]
health = perf["Health_Status"].value_counts()

SUB = ("Early-warning cost and schedule performance across a 75-project "
       "synthetic construction portfolio, 2022-2025.")


def clip(s, n=26):
    s = str(s)
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0]
    return (cut or s[:n]) + "…"


# ==========================================================  1. Executive
def executive():
    d = Dashboard("Project Controls Analytics", SUB,
                  eyebrow="Executive portfolio view")
    d.kpis([
        (f"{int(summ['Project_Count'])}", "Projects", NAVY_3),
        (money(summ["Total_BAC"]), "Portfolio BAC", NAVY_3),
        (money(summ["Total_EAC"]), "Forecast EAC", BRICK),
        (f"{summ['Forecast_Overrun_Pct']:.1%}", "Forecast overrun", RED),
        (f"{summ['Weighted_CPI']:.3f}", "Weighted CPI", RED),
        (f"{summ['Average_Delay_Days']:.1f} d", "Avg forecast delay", AMBER),
    ])

    ax = d.panel((0.0, 0.52, 0.28, 0.48), "Portfolio health",
                 "Projects by composite status", bottom=0.30)
    donut(ax, BANDS, [int(health.get(b, 0)) for b in BANDS],
          [STATUS[b] for b in BANDS], centre_value=int(summ["Project_Count"]),
          centre_label="projects", legend_below=True)

    p = ptype.sort_values("Forecast_Overrun_Pct", ascending=False)
    ax = d.panel((0.30, 0.52, 0.38, 0.48), "Forecast overrun by project type",
                 "Weighted overrun against budget at completion", left=0.34)
    cols = [RED if v > 0.10 else AMBER if v > 0.05 else GREEN
            for v in p["Forecast_Overrun_Pct"]]
    hbar(ax, [f"{clip(r.Project_Type, 24)}  (n={int(r.Project_Count)})"
              for r in p.itertuples()],
         (p["Forecast_Overrun_Pct"] * 100).tolist(), colors=cols,
         fmt=lambda v: f"{v:.1f}%")
    ax.tick_params(axis="y", labelsize=8.4)
    ax.set_xlabel("Forecast overrun (%)")

    ax = d.panel((0.70, 0.52, 0.30, 0.48), "Cost and schedule efficiency",
                 "Weighted CPI and SPI by delivery method", left=0.30)
    dm = deliv.sort_values("Weighted_CPI")
    y = np.arange(len(dm))
    ax.barh(y - 0.19, dm["Weighted_CPI"], height=0.36, color=BRICK,
            label="CPI", zorder=3)
    ax.barh(y + 0.19, dm["Weighted_SPI"], height=0.36, color=STEEL,
            label="SPI", zorder=3)
    ax.axvline(1.0, color=MUTED, linestyle="--", linewidth=1.1, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels([clip(m, 22) for m in dm["Delivery_Method"]], fontsize=8.4)
    ax.set_xlim(0.80, 1.05)
    ax.set_ylim(-0.6, len(dm) - 0.5 + 0.9)   # headroom so the legend clears the bars
    ax.grid(axis="y", visible=False)
    ax.legend(fontsize=8.8, ncol=2, loc="upper right")
    ax.set_xlabel("Index (1.00 = on plan)")

    ax = d.panel((0.0, 0.0, 1.0, 0.46), "Projects requiring management attention",
                 "Top 10 by composite risk; every row breaches at least one Red threshold",
                 left=0.02)
    t = top10.head(10)
    table_panel(
        ax,
        ["#", "Project", "Type", "Delivery", "CPI", "SPI", "Overrun",
         "Delay", "Contingency", "Status"],
        [[str(i + 1), f"{r.Project_ID}  {clip(r.Project_Name, 26)}",
          clip(r.Project_Type, 20), clip(r.Delivery_Method, 18),
          f"{r.CPI:.3f}", f"{r.SPI:.3f}", f"{r.Forecast_Overrun_Pct:.1%}",
          f"{int(r.Schedule_Delay_Days)} d",
          f"{r.Contingency_Utilization_Pct:.0%}", r.Health_Status]
         for i, r in enumerate(t.itertuples())],
        widths=[0.03, 0.275, 0.135, 0.125, 0.058, 0.058, 0.075, 0.062, 0.10, 0.062],
        aligns=["right", "left", "left", "left", "right", "right", "right",
                "right", "right", "left"],
        cell_colors={(i, 9): STATUS.get(r.Health_Status, INK)
                     for i, r in enumerate(t.itertuples())})
    d.save(OUT / "executive_dashboard.png")


# ==========================================================  2. Operational
def operational():
    d = Dashboard("Operational Drivers and Early Warning",
                  "What is moving the portfolio position, and which signals move first.",
                  eyebrow="Operational insights")
    d.kpis([
        (money(summ["Total_Approved_CO"]), "Approved change value", BRICK),
        (money(summ["Total_Pending_CO"]), "Pending exposure", AMBER),
        (f"{summ['Weighted_SPI']:.3f}", "Weighted SPI", AMBER),
        (f"{summ['Contingency_Utilization_Pct']:.1%}", "Contingency used", RED),
        (f"{int(health.get('Red', 0))}", "Red projects", RED),
        (f"{int(health.get('Green', 0))}", "Green projects", GREEN),
    ])

    ax = d.panel((0.0, 0.52, 0.50, 0.48), "Weighted CPI and SPI trend",
                 "Portfolio-weighted indices by reporting month")
    tr = trend.copy()
    tr["Reporting_Date"] = pd.to_datetime(tr["Reporting_Date"])
    ax.plot(tr["Reporting_Date"], tr["Weighted_CPI"], color=BRICK,
            linewidth=2.2, label="Weighted CPI", zorder=3)
    ax.plot(tr["Reporting_Date"], tr["Weighted_SPI"], color=STEEL,
            linewidth=2.2, label="Weighted SPI", zorder=3)
    ax.axhline(1.0, color=MUTED, linestyle="--", linewidth=1.1, zorder=2)
    ax.set_ylabel("Index")
    ax.legend(fontsize=8.8, ncol=2, loc="lower left")
    ax.grid(axis="x", visible=False)
    ax.tick_params(axis="x", labelrotation=0, labelsize=8.4)

    c = cat.sort_values("Approved_Value", ascending=False).head(6)
    ax = d.panel((0.52, 0.52, 0.48, 0.48), "Approved change value by category",
                 "Where the approved commercial exposure originates", left=0.34)
    hbar(ax, [clip(v, 26) for v in c["Change_Category"]],
         c["Approved_Value"].tolist(), color=BRICK, fmt=lambda v: money(v))
    ax.xaxis.set_major_formatter(MONEY)
    ax.tick_params(axis="y", labelsize=8.4)
    ax.set_xlabel("Approved change value")

    ax = d.panel((0.0, 0.0, 0.50, 0.46), "Tested early-warning relationships",
                 "Correlation strength; association only, not causation", left=0.42)
    cc = corr.reindex(corr["Pearson_r"].abs().sort_values(ascending=False).index).head(6)
    cols = [BRICK if v > 0 else STEEL for v in cc["Pearson_r"]]
    hbar(ax, [clip(r.replace(" vs ", "\nvs "), 44) for r in cc["Relationship"]],
         cc["Pearson_r"].abs().tolist(), colors=cols, fmt=lambda v: f"{v:.3f}")
    ax.tick_params(axis="y", labelsize=7.6)
    ax.set_xlabel("|Pearson r|")

    ax = d.panel((0.52, 0.0, 0.48, 0.46), "RFI response by discipline",
                 "Average response days; slowest first", left=0.30)
    dd = disc.sort_values("Avg_Response_Days", ascending=False).head(8)
    hbar(ax, [clip(v, 24) for v in dd["Discipline"]],
         dd["Avg_Response_Days"].tolist(), color=BRICK_2,
         fmt=lambda v: f"{v:.1f} d")
    ax.tick_params(axis="y", labelsize=8.4)
    ax.set_xlabel("Average response days")
    d.save(OUT / "operational_insights.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    print(f"Writing dashboards to {OUT}")
    executive()
    operational()
    print("done")
