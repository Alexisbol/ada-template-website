"""
Generate interactive comparison plot of PosFed vs NegFed rankings by sector
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sys
from pathlib import Path

# Add parent directory to sys.path
parent_dir = Path.cwd()
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from helpers.fed_events_analysis import *

print("Loading Fed rates and generating signals...")
df_fed_rates = pd.read_csv("fed_rate_1962_today.csv")

signals = identify_fed_rate_signals(
    df_fed_rates,
    window_size=28,
    transition_window=3,
    central_metric="robust",
    alfa=0.8,
    min_delta=0.2,
    max_delta=2,
    skip_days=5,
    stability_days=21,
    stability_fraction=0.5,
    verbose=False,
)

print(f"Processing {len(signals)} Fed rate signals...")

# Load pairs and metadata
pairs = pd.read_csv("data/ticker_sector_pairs.csv")
meta = pd.read_csv("data/symbols_valid_meta_augmented_with_dates.csv")

pval_threshold = 0.1

from collections import Counter
import os
from scipy.stats import binomtest

posfed_results, negfed_results = [], []

print("Analyzing ticker pairs...")
for idx, row in enumerate(pairs.iterrows()):
    _, row = row
    tickerA, tickerB, sector = row["tickerA"], row["tickerB"], row["sector"]
    
    if idx % 100 == 0:
        print(f"  Processed {idx}/{len(pairs)} pairs...")
    
    try:
        tickerA_path = (
            f"data/etfs+fedrate+nmv/{tickerA}.csv"
            if meta.loc[meta["Symbol"] == tickerA, "ETF"].iloc[0] == "Y"
            else f"data/stocks+fedrate+nmv/{tickerA}.csv"
        )
        tickerB_path = (
            f"data/etfs+fedrate+nmv/{tickerB}.csv"
            if meta.loc[meta["Symbol"] == tickerB, "ETF"].iloc[0] == "Y"
            else f"data/stocks+fedrate+nmv/{tickerB}.csv"
        )

        if not os.path.exists(tickerA_path) or not os.path.exists(tickerB_path):
            continue

        tickers = {
            tickerA: pd.read_csv(tickerA_path),
            tickerB: pd.read_csv(tickerB_path),
        }

        common_events = get_common_fed_event_periods(
            fed_events=signals, stocks_data=tickers, pre_days=21, post_days=21
        )

        result = fed_outperformance_area(tickers, common_events, normalize=True, metric="counts")

        n_pos_wins = result.loc[0, "Counts_Area_PosFed"]
        n_neg_wins = result.loc[0, "Counts_Area_NegFed"]
        n_pos_total = result.loc[0, "N_events_PosFed"]
        n_neg_total = result.loc[0, "N_events_NegFed"]

        pval_pos = binomtest(n_pos_wins, n_pos_total, 0.5, alternative="two-sided").pvalue
        pval_neg = binomtest(n_neg_wins, n_neg_total, 0.5, alternative="two-sided").pvalue

        if pval_pos < pval_threshold or pval_neg < pval_threshold:
            res = fed_outperformance_area(tickers, common_events, normalize=True, metric="percentage")
            data = res.loc[0].to_dict()
            data.update({"Sector": sector, "TickerA": tickerA, "TickerB": tickerB})

            if pval_pos < pval_threshold:
                posfed_results.append({**data, "fed_sign": "PosFed", "pval": pval_pos})
            if pval_neg < pval_threshold:
                negfed_results.append({**data, "fed_sign": "NegFed", "pval": pval_neg})

    except Exception:
        continue

df_posFed = pd.DataFrame(posfed_results)
df_negFed = pd.DataFrame(negfed_results)

print(f"Found {len(df_posFed)} significant PosFed results")
print(f"Found {len(df_negFed)} significant NegFed results")

# Count wins by sector function
def count_wins_by_sector(df, fed_type="PosFed"):
    col = f"Percentage_Area_{fed_type}"
    winners_by_sector = []
    matches_by_sector = []

    for _, row in df.iterrows():
        sector = row["Sector"]
        val = row.get(col, None)
        if pd.isna(val):
            continue

        tickerA, tickerB = row["TickerA"], row["TickerB"]
        matches_by_sector.extend([(sector, tickerA), (sector, tickerB)])

        if val > 50:
            winners_by_sector.append((sector, tickerA))
        elif val < 50:
            winners_by_sector.append((sector, tickerB))

    win_counts = Counter(winners_by_sector)
    match_counts = Counter(matches_by_sector)

    data = []
    for (sector, ticker), total_matches in match_counts.items():
        wins = win_counts.get((sector, ticker), 0)
        data.append((sector, ticker, wins))

    out = (
        pd.DataFrame(data, columns=["Sector", "Ticker", "Wins"])
        .sort_values(["Sector", "Wins"], ascending=[True, False])
        .reset_index(drop=True)
    )
    return out

print("Computing win rankings...")
df_posWins = count_wins_by_sector(df_posFed, fed_type="PosFed")
df_negWins = count_wins_by_sector(df_negFed, fed_type="NegFed")

# Create comparison dataset
min_wins = 2
common_tickers = set(df_posWins["Ticker"]).intersection(df_negWins["Ticker"])
print(f"Common tickers found: {len(common_tickers)}")

df_pos_common = df_posWins[df_posWins["Ticker"].isin(common_tickers) & (df_posWins["Wins"] >= min_wins)].copy()
df_neg_common = df_negWins[df_negWins["Ticker"].isin(common_tickers) & (df_negWins["Wins"] >= min_wins)].copy()

df_compare = pd.merge(
    df_pos_common[["Sector", "Ticker", "Wins"]],
    df_neg_common[["Sector", "Ticker", "Wins"]],
    on=["Sector", "Ticker"],
    suffixes=("_Pos", "_Neg"),
)

# Exclude Consumer Cyclical if needed
df_compare = df_compare[df_compare["Sector"] != "Consumer Cyclical"]

# Compute ranks after filter
def compute_ranks_after_filter(df):
    ranked = []
    for sector, group in df.groupby("Sector"):
        group = group.sort_values("Wins_Pos", ascending=False).copy()
        group["PosRank"] = range(1, len(group) + 1)
        group = group.sort_values("Wins_Neg", ascending=False).copy()
        group["NegRank"] = range(1, len(group) + 1)
        ranked.append(group)
    return pd.concat(ranked, ignore_index=True)

df_compare = compute_ranks_after_filter(df_compare)

print("Creating interactive comparison plot...")

# Calculate dynamic limits
xmax = df_compare["PosRank"].max()
ymax = df_compare["NegRank"].max()
lim = max(xmax, ymax) + 1

# Consistent palette
sectors = sorted(df_compare["Sector"].unique())
sector_colors = px.colors.qualitative.Plotly
color_map = {sec: sector_colors[i % len(sector_colors)] for i, sec in enumerate(sectors)}

# Create figure
fig = go.Figure()

for sec in sectors:
    subset = df_compare[df_compare["Sector"] == sec]
    fig.add_trace(
        go.Scatter(
            x=subset["PosRank"],
            y=subset["NegRank"],
            mode="markers",
            name=sec,
            marker=dict(size=10, opacity=0.8, color=color_map[sec]),
            text=subset["Ticker"],
            customdata=subset[["Wins_Pos", "Wins_Neg"]],
            hovertemplate=(
                "<b>%{text}</b><br>"
                "Sector: " + sec + "<br>"
                "Rank PosFed: %{x}<br>"
                "Rank NegFed: %{y}<br>"
                "Wins PosFed: %{customdata[0]}<br>"
                "Wins NegFed: %{customdata[1]}<extra></extra>"
            ),
            visible=True if sec == sectors[0] else False,
        )
    )

# Reference diagonal
fig.add_shape(
    type="line",
    x0=1, y0=1,
    x1=lim, y1=lim,
    line=dict(color="gray", dash="dot", width=1),
)

# Axes
fig.update_xaxes(
    autorange="reversed",
    range=[lim, 0],
    title="Rank PosFed (1 = best)",
)
fig.update_yaxes(
    autorange="reversed",
    range=[lim, 0],
    title="Rank NegFed (1 = best)",
)

# Dropdown buttons
buttons = [
    dict(
        label="All",
        method="update",
        args=[
            {"visible": [True] * len(sectors)},
            {"title": "🔀 Comparison of PosFed vs NegFed Rankings (All Sectors)"},
        ],
    )
]
for i, sec in enumerate(sectors):
    vis = [False] * len(sectors)
    vis[i] = True
    buttons.append(
        dict(
            label=sec,
            method="update",
            args=[
                {"visible": vis},
                {"title": f"🔀 Sector: {sec}"},
            ],
        )
    )

# Final layout
fig.update_layout(
    updatemenus=[
        dict(
            buttons=buttons,
            direction="down",
            showactive=True,
            x=1.04,
            xanchor="left",
            y=1.13,
            yanchor="top",
        )
    ],
    width=750,
    height=600,
    template="plotly_white",
    legend_title_text="Sector",
    hoverlabel=dict(bgcolor="white", font_size=12),
    title=f"🔀 Comparison of PosFed vs NegFed Rankings — Initial sector: {sectors[0]}",
)

# Save to HTML
output_path = "assets/html/posfed_negfed_comparison.html"
fig.write_html(output_path)
print(f"✅ Interactive comparison plot saved to {output_path}")
