"""
Construction Project Controls Analytics - chart generation.

Regenerates every figure in share/assets/ directly from the analytical CSV
outputs in analysis/tables/. Charts are deterministic: same inputs, same output.

Usage:
    python analysis/visualization/generate_charts.py

Data disclosure: all records are synthetic. See documentation/dataset_methodology.md.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "analysis" / "tables"
ASSETS = ROOT / "share" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# House style — In Project design system
# Tokens mirror inproject-website/src/index.css and
# inproject-ai-agents/public/site.css so charts, web and report stay in step.
# --------------------------------------------------------------------------
NAVY = "#02000B"       # --navy / --ink : headings
INK = "#272421"        # --text : body copy
BRICK = "#A04732"      # --brick / --terracotta : primary accent
BRICK_2 = "#BD5A43"    # --terracotta-2
STEEL = "#53616D"      # --steel : secondary series
SAGE = "#647267"       # --sage : tertiary series
AMBER = "#C8881F"      # --amber
RED = "#C0492F"        # --red
GREEN = "#3F9D6B"      # --green
GREY = "#6E6861"       # --muted
LIGHT = "#EDEAE2"      # --beige : KPI tiles
LINE = "#DCD4C8"       # --line : axes and gridlines
PAPER = "#FFFDF8"      # --paper : figure background

# Brand faces: Source Sans 3 (body) and Roboto Slab (display).
FONT_BODY = "Source Sans 3"
FONT_DISPLAY = "Roboto Slab"

STATUS_COLORS = {"Red": RED, "Yellow": AMBER, "Green": GREEN}

plt.rcParams.update({
    "figure.dpi": 160,
    "savefig.dpi": 160,
    "savefig.bbox": "tight",
    "savefig.facecolor": PAPER,
    "figure.facecolor": PAPER,
    "font.family": [FONT_BODY, "DejaVu Sans"],
    "font.size": 10,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlecolor": NAVY,
    "axes.labelsize": 10,
    "axes.labelcolor": INK,
    "axes.edgecolor": LINE,
    "axes.facecolor": PAPER,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": LINE,
    "grid.linewidth": 0.7,
    "xtick.color": GREY,
    "ytick.color": GREY,
    "legend.frameon": False,
})


def read(name: str) -> pd.DataFrame:
    """Read an analysis table, tolerating the UTF-8 BOM written by Excel."""
    return pd.read_csv(TABLES / name, encoding="utf-8-sig")


def strip_spines(ax, keep=("left", "bottom")):
    for side in ("top", "right", "left", "bottom"):
        if side not in keep:
            ax.spines[side].set_visible(False)


def footnote(fig, text="Synthetic portfolio data - illustrative only; not an industry benchmark."):
    fig.text(0.5, -0.035, text, ha="center", fontsize=8, color=GREY, style="italic")


def save(fig, name: str):
    """Apply the display face to every title, then write the figure."""
    for ax in fig.axes:
        t = ax.title
        if t.get_text():
            t.set_fontfamily(FONT_DISPLAY)
            t.set_fontweight("bold")
    if fig._suptitle is not None:
        fig._suptitle.set_fontfamily(FONT_DISPLAY)

    out = ASSETS / name
    fig.savefig(out)
    plt.close(fig)
    print(f"  wrote {out.relative_to(ROOT)}")


pct = FuncFormatter(lambda v, _: f"{v * 100:.0f}%")


# --------------------------------------------------------------------------
# 1. Portfolio health overview
# --------------------------------------------------------------------------
def chart_portfolio_health():
    s = read("portfolio_summary.csv").set_index("Metric")["Value"]
    counts = {
        "Red": int(s["Red_Projects"]),
        "Yellow": int(s["Yellow_Projects"]),
        "Green": int(s["Green_Projects"]),
    }
    total = sum(counts.values())

    fig = plt.figure(figsize=(11, 4.6))
    grid = fig.add_gridspec(1, 2, width_ratios=[1.15, 1], wspace=0.28)

    # Donut
    ax = fig.add_subplot(grid[0, 0])
    wedges, _ = ax.pie(
        list(counts.values()),
        colors=[STATUS_COLORS[k] for k in counts],
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.42, "edgecolor": PAPER, "linewidth": 2},
    )
    ax.text(0, 0.10, f"{total}", ha="center", va="center",
            fontsize=30, fontweight="bold", color=NAVY)
    ax.text(0, -0.22, "projects", ha="center", va="center", fontsize=10, color=GREY)
    ax.set_title("Portfolio health distribution", pad=14)
    ax.legend(
        wedges,
        [f"{k} - {v} ({v / total:.0%})" for k, v in counts.items()],
        loc="upper center", bbox_to_anchor=(0.5, 0.03), ncol=3,
        fontsize=9.5, columnspacing=1.2, handlelength=1.1,
    )

    # KPI panel
    ax = fig.add_subplot(grid[0, 1])
    ax.axis("off")
    kpis = [
        ("Budget at completion", f"${s['Total_BAC'] / 1e9:.2f}B", NAVY),
        ("Forecast at completion", f"${s['Total_EAC'] / 1e9:.2f}B", NAVY),
        ("Forecast overrun", f"{s['Forecast_Overrun_Pct']:.1%}", RED),
        ("Weighted CPI", f"{s['Weighted_CPI']:.3f}", RED),
        ("Weighted SPI", f"{s['Weighted_SPI']:.3f}", AMBER),
        ("Contingency utilisation", f"{s['Contingency_Utilization_Pct']:.1%}", AMBER),
    ]
    for i, (label, value, colour) in enumerate(kpis):
        row, col = divmod(i, 2)
        x, y = col * 0.5, 0.80 - row * 0.30
        ax.add_patch(plt.Rectangle((x, y - 0.185), 0.46, 0.245,
                                   facecolor=LIGHT, edgecolor="none",
                                   transform=ax.transAxes))
        ax.text(x + 0.03, y - 0.01, label, transform=ax.transAxes,
                fontsize=8.4, color=GREY)
        ax.text(x + 0.03, y - 0.13, value, transform=ax.transAxes,
                fontsize=17, fontweight="bold", color=colour)
    ax.set_title("Portfolio position", pad=14, loc="left")

    footnote(fig)
    save(fig, "portfolio_health_overview.png")


# --------------------------------------------------------------------------
# 2. Monthly CPI / SPI trend
# --------------------------------------------------------------------------
def chart_cpi_spi_trend():
    df = read("monthly_portfolio_trend.csv")
    df["Reporting_Date"] = pd.to_datetime(df["Reporting_Date"])

    fig, ax = plt.subplots(figsize=(11, 4.4))
    ax.axhspan(0.0, 0.90, color=RED, alpha=0.055)
    ax.axhline(1.0, color=GREY, ls="--", lw=1, zorder=1)
    ax.axhline(0.90, color=RED, ls=":", lw=1.1, zorder=1)

    ax.plot(df["Reporting_Date"], df["Weighted_CPI"], color=BRICK, lw=2.4,
            label="Weighted CPI (cost)")
    ax.plot(df["Reporting_Date"], df["Weighted_SPI"], color=STEEL, lw=2.4,
            label="Weighted SPI (schedule)")

    for col, colour in (("Weighted_CPI", BRICK), ("Weighted_SPI", STEEL)):
        ax.scatter(df["Reporting_Date"].iloc[-1], df[col].iloc[-1],
                   color=colour, s=42, zorder=5)
        ax.annotate(f"{df[col].iloc[-1]:.3f}",
                    (df["Reporting_Date"].iloc[-1], df[col].iloc[-1]),
                    xytext=(9, 0), textcoords="offset points",
                    va="center", fontsize=9.5, fontweight="bold", color=colour)

    ax.text(df["Reporting_Date"].iloc[1], 0.882, "CPI < 0.90 - critical trigger",
            fontsize=8.4, color=RED, style="italic")
    ax.set_ylim(0.82, 1.03)
    ax.set_ylabel("Index value")
    ax.set_title("Portfolio cost and schedule performance never recovered to plan", pad=12)
    ax.legend(loc="lower left", ncol=2, fontsize=9.5)
    strip_spines(ax)
    footnote(fig)
    save(fig, "cpi_spi_trend.png")


# --------------------------------------------------------------------------
# 3. Forecast overrun by project type
# --------------------------------------------------------------------------
def chart_overrun_by_type():
    df = read("project_type_summary.csv").sort_values("Forecast_Overrun_Pct")

    fig, ax = plt.subplots(figsize=(10, 4.6))
    colours = [RED if v >= 0.13 else AMBER if v >= 0.11 else GREEN
               for v in df["Forecast_Overrun_Pct"]]
    bars = ax.barh(df["Project_Type"], df["Forecast_Overrun_Pct"],
                   color=colours, height=0.62)
    for bar, (_, r) in zip(bars, df.iterrows()):
        ax.text(bar.get_width() + 0.0035, bar.get_y() + bar.get_height() / 2,
                f"{r['Forecast_Overrun_Pct']:.1%}   (n={int(r['Project_Count'])})",
                va="center", fontsize=9, color=INK)

    ax.xaxis.set_major_formatter(pct)
    ax.set_xticks(np.arange(0, 0.21, 0.05))
    ax.set_xlim(0, df["Forecast_Overrun_Pct"].max() * 1.30)
    ax.set_xlabel("Forecast overrun (% of budget at completion)")
    ax.set_title("Mixed-Use carries the highest forecast overrun; Heavy Civil the lowest", pad=12)
    ax.grid(axis="y", visible=False)
    strip_spines(ax)
    footnote(fig)
    save(fig, "forecast_overrun_by_project_type.png")


# --------------------------------------------------------------------------
# 4. Early-warning correlations
# --------------------------------------------------------------------------
def chart_correlations():
    corr = read("correlation_summary.csv")
    proj = read("project_performance_analysis.csv")

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5))

    panels = [
        ("Contingency_Burn_Ratio", "Forecast_Overrun_Pct",
         "Contingency Burn Ratio vs Forecast Overrun %",
         "Contingency burn ratio", "Forecast overrun", BRICK, True),
        ("Avg_RFI_Response_Days", "Schedule_Delay_Days",
         "Average RFI Response Days vs Schedule Delay Days",
         "Average RFI response (days)", "Schedule delay (days)", STEEL, False),
    ]

    for ax, (xcol, ycol, key, xlabel, ylabel, colour, ypct) in zip(axes, panels):
        row = corr.loc[corr["Relationship"] == key].iloc[0]
        x, y = proj[xcol].astype(float), proj[ycol].astype(float)
        pt_colours = proj["Health_Status"].map(STATUS_COLORS).fillna(GREY)

        ax.scatter(x, y, c=pt_colours, s=34, alpha=0.75,
                   edgecolor=PAPER, linewidth=0.6, zorder=3)
        slope, intercept = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 100)
        ax.plot(xs, slope * xs + intercept, color=colour, lw=2, zorder=4)

        ax.text(0.035, 0.94,
                f"r = {row['Pearson_r']:.3f}   R² = {row['R_Squared']:.3f}\n{row['Strength']} positive",
                transform=ax.transAxes, va="top", fontsize=9.5,
                fontweight="bold", color=NAVY,
                bbox=dict(boxstyle="round,pad=0.45", facecolor=LIGHT, edgecolor="none"))

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        if ypct:
            ax.yaxis.set_major_formatter(pct)
        strip_spines(ax)

    axes[0].set_title("Strongest early-warning signal", pad=10)
    axes[1].set_title("Moderate schedule signal", pad=10)

    handles = [plt.Line2D([], [], marker="o", ls="", markersize=7,
                          markerfacecolor=c, markeredgecolor=PAPER, label=k)
               for k, c in STATUS_COLORS.items()]
    fig.suptitle("Contingency burn is the leading indicator of cost overrun",
                 fontsize=13.5, fontweight="bold", color=NAVY, fontfamily=FONT_DISPLAY, y=1.02)
    fig.tight_layout()
    fig.legend(handles=handles, loc="lower center", ncol=3,
               bbox_to_anchor=(0.5, -0.06), fontsize=9.5)
    fig.text(0.5, -0.135,
             "Each point is one project, coloured by health status. "
             "Synthetic portfolio data - correlation does not establish causation.",
             ha="center", fontsize=8, color=GREY, style="italic")
    save(fig, "early_warning_correlations.png")


# --------------------------------------------------------------------------
# 5. Top 10 projects requiring attention
# --------------------------------------------------------------------------
def chart_top_risk():
    df = read("top_10_risk_projects.csv").sort_values("Forecast_Overrun_Pct")
    labels = [f"{r.Project_ID}  {r.Project_Name}" for r in df.itertuples()]

    fig, ax = plt.subplots(figsize=(10.5, 5.0))
    bars = ax.barh(labels, df["Forecast_Overrun_Pct"],
                   color=[STATUS_COLORS.get(s, GREY) for s in df["Health_Status"]],
                   height=0.64)
    for bar, (_, r) in zip(bars, df.iterrows()):
        ax.text(bar.get_width() + 0.006, bar.get_y() + bar.get_height() / 2,
                f"{r['Forecast_Overrun_Pct']:.1%}   CPI {r['CPI']:.2f}   {int(r['Schedule_Delay_Days'])}d late",
                va="center", fontsize=8.6, color=INK)

    ax.xaxis.set_major_formatter(pct)
    ax.set_xlim(0, df["Forecast_Overrun_Pct"].max() * 1.42)
    ax.set_xlabel("Forecast overrun (% of budget at completion)")
    ax.set_title("Top 10 projects requiring management attention", pad=12)
    ax.tick_params(axis="y", labelsize=8.8)
    ax.grid(axis="y", visible=False)
    strip_spines(ax)
    footnote(fig)
    save(fig, "top_10_risk_projects.png")


# --------------------------------------------------------------------------
# 6. Change orders by category
# --------------------------------------------------------------------------
def chart_change_orders():
    df = read("change_category_summary.csv").sort_values("Approved_Value")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)

    value_m = df["Approved_Value"] / 1e6
    axes[0].barh(df["Change_Category"], value_m, color=BRICK, height=0.62)
    for i, v in enumerate(value_m):
        axes[0].text(v + 0.7, i, f"${v:.1f}M", va="center", fontsize=9, color=INK)
    axes[0].set_xlabel("Approved change-order value ($M)")
    axes[0].set_title("Approved value", pad=10)
    axes[0].set_xlim(0, value_m.max() * 1.22)

    days = df["Approved_Schedule_Impact_Days"]
    axes[1].barh(df["Change_Category"], days, color=AMBER, height=0.62)
    for i, v in enumerate(days):
        axes[1].text(v + 11, i, f"{int(v)}d", va="center", fontsize=9, color=INK)
    axes[1].set_xlabel("Approved schedule impact (days)")
    axes[1].set_title("Schedule impact", pad=10)
    axes[1].set_xlim(0, days.max() * 1.22)

    for ax in axes:
        ax.grid(axis="y", visible=False)
        strip_spines(ax)

    fig.suptitle("Owner-directed changes drive cost; unforeseen conditions drive delay",
                 fontsize=13.5, fontweight="bold", color=NAVY, fontfamily=FONT_DISPLAY, y=1.02)
    fig.tight_layout()
    footnote(fig)
    save(fig, "change_orders_by_category.png")


# --------------------------------------------------------------------------
# 7. RFI performance by discipline
# --------------------------------------------------------------------------
def chart_rfi_discipline():
    df = read("rfi_discipline_summary.csv").sort_values("Avg_Response_Days")

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4), sharey=True)

    axes[0].barh(df["Discipline"], df["Avg_Response_Days"], color=BRICK, height=0.6)
    for i, v in enumerate(df["Avg_Response_Days"]):
        axes[0].text(v + 0.18, i, f"{v:.1f}d", va="center", fontsize=9, color=INK)
    axes[0].set_xlabel("Average response time (days)")
    axes[0].set_title("RFI response time", pad=10)
    axes[0].set_xlim(0, df["Avg_Response_Days"].max() * 1.20)

    late_col = "Late_RFI_Rate" if "Late_RFI_Rate" in df.columns else "Late_Rate"
    axes[1].barh(df["Discipline"], df[late_col], color=AMBER, height=0.6)
    for i, v in enumerate(df[late_col]):
        axes[1].text(v + 0.012, i, f"{v:.0%}", va="center", fontsize=9, color=INK)
    axes[1].set_xlabel("Late RFI rate")
    axes[1].set_title("Share of RFIs answered late", pad=10)
    axes[1].xaxis.set_major_formatter(pct)
    axes[1].set_xlim(0, 1.0)

    for ax in axes:
        ax.grid(axis="y", visible=False)
        strip_spines(ax)

    fig.suptitle("Every discipline exceeds a 70% late-RFI rate",
                 fontsize=13.5, fontweight="bold", color=NAVY, fontfamily=FONT_DISPLAY, y=1.02)
    footnote(fig)
    fig.tight_layout()
    save(fig, "rfi_performance_by_discipline.png")


# --------------------------------------------------------------------------
def main():
    print("Generating charts from analysis/tables/ ...")
    chart_portfolio_health()
    chart_cpi_spi_trend()
    chart_overrun_by_type()
    chart_correlations()
    chart_top_risk()
    chart_change_orders()
    chart_rfi_discipline()
    print("Done.")


if __name__ == "__main__":
    main()
