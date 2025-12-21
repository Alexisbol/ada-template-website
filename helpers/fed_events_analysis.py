import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple, Literal,Dict
from matplotlib.lines import Line2D
from datetime import timedelta
from itertools import combinations


def identify_fed_rate_signals(
    df: pd.DataFrame,
    window_size: int = 30,
    transition_window: int = 3,
    central_metric: Literal["mean", "median", "robust"] = "robust",
    alfa: float = 0.5,
    min_delta: float = 0.5,
    max_delta: float = 3.0,
    skip_days: int = 5,
    stability_days: int = 21,
    stability_fraction: float = 0.5,
    verbose: bool = False,
) -> List[Tuple[str, str, float]]:
    """
    Identify interesting periods for Fed rate analysis based on significant
    rate changes and subsequent stability.

    The algorithm uses a sliding window to establish a baseline Fed rate, then
    searches within a transition window for the most significant deviation
    (signals) that are followed by periods of relative stability.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing 'Time Period' and 'RIFSPFF_N.D' columns
    window_size : int, default=30
        Number of days in the sliding window for baseline calculation
    transition_window : int, default=3
        Number of days to search ahead for the maximum delta.
        The day with the largest absolute change will be selected as signal start.
    central_metric : {'mean', 'median', 'robust'}, default='robust'
        Statistical metric to use as the center of the sliding window baseline.
        'robust' uses the average of mean and median.
    alfa : float, default=0.5
        Fraction of standard deviation to define uncertainty range around
        both the baseline and the delta
    min_delta : float, default=0.5
        Minimum absolute change in Fed rate (%) to qualify as a signal.
        The entire uncertainty range must be above this threshold.
    max_delta : float, default=3.0
        Maximum absolute change in Fed rate (%) to qualify as a signal.
        The entire uncertainty range must be below this threshold.
    skip_days : int, default=5
        Number of days to skip after identifying a signal to avoid
        detecting consecutive related signals
    stability_days : int, default=21
        Number of days following a signal to check for stability
    stability_fraction : float, default=0.5
        Fraction of delta_f to define the acceptable stability range.
        E.g., 0.5 means Fed rate can vary by ±50% of the initial change.
    verbose : bool, default=False
        If True, print progress information about signal detection

    Returns
    -------
    List[Tuple[str, str, float]]
        List of identified periods, each containing:
        - start_date: Date when the signal occurred (YYYY-MM-DD)
        - end_date: End of the stability period (YYYY-MM-DD)
        - delta_f: The Fed rate change that occurred (%)
    """
    df = df.copy()
    df = df.rename(columns={"Time Period": "Date", "RIFSPFF_N.D": "Fed_rate"})
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    if verbose:
        print(f"Analyzing {len(df)} days of Fed rate data")
        print(
            f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to "
            f"{df['Date'].max().strftime('%Y-%m-%d')}\n"
        )

    signals = []
    candidates_found = 0
    candidates_delta_rejected = 0
    candidates_stability_rejected = 0

    i = window_size

    while i < len(df) - stability_days - transition_window:
        window = df["Fed_rate"].iloc[i - window_size : i]

        if central_metric == "mean":
            baseline = window.mean()
        elif central_metric == "median":
            baseline = window.median()
        else: 
            baseline = (window.mean() + window.median()) / 2

        std = window.std()

        max_abs_delta = 0
        best_day_offset = 0
        best_delta = 0

        for offset in range(transition_window):
            if i + offset >= len(df):
                break

            rate = df["Fed_rate"].iloc[i + offset]
            delta = rate - baseline
            abs_delta = abs(delta)

            if abs_delta > max_abs_delta:
                max_abs_delta = abs_delta
                best_day_offset = offset
                best_delta = delta

        signal_day = i + best_day_offset
        delta_f = best_delta

        uncertainty = alfa * std
        abs_delta_min = abs(delta_f) - uncertainty
        abs_delta_max = abs(delta_f) + uncertainty

        if abs_delta_min >= min_delta and abs_delta_max <= max_delta:
            candidates_found += 1

            if signal_day + stability_days >= len(df):
                i += 1
                continue

            next_rate = df["Fed_rate"].iloc[signal_day]

            stability_margin = stability_fraction * abs(delta_f)
            stability_range_lower = next_rate - stability_margin
            stability_range_upper = next_rate + stability_margin

            future_rates = df["Fed_rate"].iloc[
                signal_day : signal_day + stability_days + 1
            ]
            is_stable = future_rates.between(
                stability_range_lower, stability_range_upper
            ).all()

            if is_stable:
                start_date = df["Date"].iloc[signal_day].strftime("%Y-%m-%d")
                end_date = df["Date"].iloc[
                    signal_day + stability_days
                ].strftime("%Y-%m-%d")
                signals.append((start_date, end_date, round(delta_f, 4)))

                if verbose:
                    print(
                        f"✓ Signal found: {start_date} | "
                        f"Δ={delta_f:+.4f}% | stable until {end_date}"
                    )

                i = signal_day + skip_days
                continue
            else:
                candidates_stability_rejected += 1
        elif max_abs_delta > 0:
            if abs_delta_min < min_delta or abs_delta_max > max_delta:
                candidates_delta_rejected += 1

        i += 1

    if verbose:
        print(f"\n{'='*60}")
        print(f"Summary:")
        print(f"  Candidate events found: {candidates_found}")
        print(
            f"  Rejected (delta out of range): {candidates_delta_rejected}"
        )
        print(
            f"  Rejected (insufficient stability): "
            f"{candidates_stability_rejected}"
        )
        print(f"  Final signals identified: {len(signals)}")
        print(f"{'='*60}\n")

    return signals




def plot_fed_rate_overview(
    df: pd.DataFrame,
    signals: List[Tuple[str, str, float]],
    figsize: Tuple[int, int] = (18, 6),
) -> None:
    """
    Plot an overview of the entire Fed rate history with all detected signals.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing 'Time Period' and 'RIFSPFF_N.D' columns
    signals : List[Tuple[str, str, float]]
        Output from identify_fed_rate_signals()
    figsize : Tuple[int, int], default=(18, 6)
        Figure size (width, height) in inches
    """
    if not signals:
        print("No signals to plot.")
        return

    df = df.copy()
    df = df.rename(columns={"Time Period": "Date", "RIFSPFF_N.D": "Fed_rate"})
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(
        df["Date"],
        df["Fed_rate"],
        color="steelblue",
        linewidth=2,
        label="Fed Rate",
        zorder=2,
    )

    for start, end, delta_f in signals:
        start_date = pd.to_datetime(start)
        color = "red" if delta_f > 0 else "green"
        ax.axvline(
            start_date,
            color=color,
            linestyle="--",
            linewidth=1.5,
            alpha=0.7,
            zorder=1,
        )

   

    legend_elements = [
        Line2D([0], [0], color="steelblue", linewidth=2, label="Fed Rate"),
        Line2D(
            [0],
            [0],
            color="red",
            linestyle="--",
            linewidth=1.5,
            label="Rate Increase",
        ),
        Line2D(
            [0],
            [0],
            color="green",
            linestyle="--",
            linewidth=1.5,
            label="Rate Decrease",
        ),
    ]

    ax.set_title(
        f"Fed Rate Overview — {len(signals)} Events Detected",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Date", fontsize=12, fontweight="bold")
    ax.set_ylabel("Fed Rate (%)", fontsize=12, fontweight="bold")
    ax.legend(handles=legend_elements, loc="best", fontsize=10, framealpha=0.95)
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.show()


def plot_single_fed_rate_period(
    df: pd.DataFrame,
    signals: List[Tuple[str, str, float]],
    window_size: int = 30,
    central_metric: Literal["mean", "median", "robust"] = "robust",
    alfa: float = 0.5,
    stability_fraction: float = 0.5,
    period_index: int = 0,
    figsize: Tuple[int, int] = (14, 6),
    pre_event_days: int = 45,
    post_event_days: int = 30,
    show: bool = True,
) -> None:
    """
    Plot a single Fed rate signal period with baseline and stability
    visualization.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing 'Time Period' and 'RIFSPFF_N.D' columns
    signals : List[Tuple[str, str, float]]
        Output from identify_fed_rate_signals()
    window_size : int, default=30
        Number of days in the sliding window for baseline calculation
    central_metric : {'mean', 'median', 'robust'}, default='robust'
        Statistical metric for the baseline center
    alfa : float, default=0.5
        Fraction of std dev for uncertainty range around baseline
    stability_fraction : float, default=0.5
        Fraction of delta_f defining the stability range
    period_index : int, default=0
        Index of the signal period to visualize (0-based)
    figsize : Tuple[int, int], default=(14, 6)
        Figure size (width, height) in inches
    pre_event_days : int, default=45
        Number of days to show before the signal
    post_event_days : int, default=30
        Number of days to show after the stability period ends
    """
    if not signals:
        print("No signals to plot.")
        return

    if period_index < 0 or period_index >= len(signals):
        raise IndexError(f"Invalid period_index: choose 0–{len(signals)-1}")

    start, end, delta_f = signals[period_index]
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)

    df = df.copy()
    df = df.rename(columns={"Time Period": "Date", "RIFSPFF_N.D": "Fed_rate"})
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    idx = df.index[df["Date"] == start_date]
    if len(idx) == 0:
        print(f"Start date {start_date} not found in DataFrame.")
        return

    i = idx[0]

    if i < window_size:
        print("Not enough historical data for baseline calculation.")
        return

    window = df["Fed_rate"].iloc[i - window_size : i]

    if central_metric == "mean":
        baseline = window.mean()
    elif central_metric == "median":
        baseline = window.median()
    else:  # robust
        baseline = (window.mean() + window.median()) / 2

    std = window.std()
    uncertainty = alfa * std

    baseline_lower = baseline - uncertainty
    baseline_upper = baseline + uncertainty

    next_rate = df["Fed_rate"].iloc[i]

    stability_margin = stability_fraction * abs(delta_f)
    stability_lower = next_rate - stability_margin
    stability_upper = next_rate + stability_margin

    plot_start = start_date - pd.Timedelta(days=pre_event_days)
    plot_end = end_date + pd.Timedelta(days=post_event_days)
    mask = (df["Date"] >= plot_start) & (df["Date"] <= plot_end)
    df_focus = df.loc[mask]

    fig, ax = plt.subplots(figsize=figsize)

    ax.plot(
        df_focus["Date"],
        df_focus["Fed_rate"],
        color="steelblue",
        linewidth=2.5,
        label="Fed Rate",
        zorder=3,
    )

    baseline_end = start_date
    baseline_start = df_focus["Date"].min()

    ax.hlines(
        baseline,
        xmin=baseline_start,
        xmax=baseline_end,
        colors="dimgray",
        linestyles="--",
        linewidth=2,
        label=f"Baseline ({central_metric}) = {baseline:.2f}%",
        zorder=2,
    )

    ax.fill_between(
        [baseline_start, baseline_end],
        baseline_lower,
        baseline_upper,
        color="gray",
        alpha=0.2,
        label=f"Baseline uncertainty (±{alfa}σ)",
        zorder=1,
    )

    stability_mask = (df_focus["Date"] >= start_date) & (df_focus["Date"] <= end_date)
    df_stability = df_focus[stability_mask]

    ax.fill_between(
        df_stability["Date"],
        stability_lower,
        stability_upper,
        color="lightgreen",
        alpha=0.25,
        label=f"Stability range (±{stability_fraction*100:.0f}% of Δ)",
        zorder=1,
    )

    ax.axvline(
        start_date,
        color="red",
        linestyle="--",
        linewidth=2,
        alpha=0.8,
        label=f"Signal start (Δ={delta_f:+.2f}%)",
        zorder=3,
    )

    ax.axvline(
        end_date,
        color="orange",
        linestyle="--",
        linewidth=2,
        alpha=0.7,
        label=f"Stability end",
        zorder=3,
    )

    ax.set_title(
        f"Fed Rate Event Analysis — {start}",
        fontsize=14,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Date", fontsize=12, fontweight="bold")
    ax.set_ylabel("Fed Rate (%)", fontsize=12, fontweight="bold")
    ax.legend(loc="best", fontsize=9, framealpha=0.95)
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    if show==True:
        plt.show()
    else:
        plt.savefig(f"../assets/img/fed_rate_event_{period_index+1}.png")
    


def plot_all_fed_rate_periods(
    df: pd.DataFrame,
    signals: List[Tuple[str, str, float]],
    window_size: int = 30,
    central_metric: Literal["mean", "median", "robust"] = "robust",
    alfa: float = 0.5,
    stability_fraction: float = 0.5,
    pre_event_days: int = 45,
    post_event_days: int = 30,
) -> None:

    if not signals:
        print("No signals to plot.")
        return

    print(f"Plotting overview with {len(signals)} events...")
    plot_fed_rate_overview(df, signals)

    print(f"\nPlotting {len(signals)} individual event periods...\n")
    for idx in range(len(signals)):
        print(f"Event {idx + 1}/{len(signals)}: {signals[idx][0]}")
        plot_single_fed_rate_period(
            df=df,
            signals=signals,
            window_size=window_size,
            central_metric=central_metric,
            alfa=alfa,
            stability_fraction=stability_fraction,
            period_index=idx,
            pre_event_days=pre_event_days,
            post_event_days=post_event_days,
        )


def plot_fed_event_reactions(
    stocks_data: Dict[str, pd.DataFrame],
    event_date: str,
    pre_days: int = 10,
    post_days: int = 10,
    price_col: str = "Adj Close",
):
    event_date = pd.to_datetime(event_date)
    plt.figure(figsize=(10, 6))

    for symbol, df in stocks_data.items():
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.set_index("Date").sort_index()

        if event_date not in df.index:
            print(f"⚠️ {symbol}: event date not available in data.")
            continue

        start_date = event_date - timedelta(days=pre_days)
        end_date = event_date + timedelta(days=post_days)

        window = df.loc[start_date:end_date, price_col]
        if window.empty:
            print(f"⚠️ Insufficient data for {symbol}.")
            continue

        base_price = window.loc[event_date]
        rel_return = (window / base_price - 1) * 100
        rel_index = (window.index - event_date).days

        plt.plot(rel_index, rel_return, label=symbol)

    plt.axvline(0, color="black", linestyle="--", linewidth=0.8)
    plt.axhline(0, color="gray", linestyle=":")
    plt.title(f"Stock performance relative to Fed event ({event_date.date()})")
    plt.xlabel("Days relative to the event")
    plt.ylabel("Price change relative to event day (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



def get_common_fed_event_periods(
    fed_events: List[Tuple[str, str, float]],
    stocks_data: Dict[str, pd.DataFrame],
    pre_days: int = 21,
    post_days: int = 21,
    date_col: str = "Date",
) -> pd.DataFrame:
   
    coverage = {}
    for sym, df in stocks_data.items():
        d = df.copy()
        d[date_col] = pd.to_datetime(d[date_col])
        coverage[sym] = (d[date_col].min(), d[date_col].max())

    valid_events = []
    for start_str, end_str, delta_fed in fed_events:
        start_dt = pd.to_datetime(start_str)
        end_dt = pd.to_datetime(end_str)

        ok = True
        for sym, (start_cov, end_cov) in coverage.items():
            if start_dt - timedelta(days=pre_days) < start_cov or end_dt + timedelta(days=post_days) > end_cov:
                ok = False
                break

        if ok:
            valid_events.append({
                "Start": start_dt,
                "End": end_dt,
                "Delta_Fed": float(delta_fed)
            })

    return pd.DataFrame(valid_events)


def fed_outperformance_area(
    stocks_data: Dict[str, pd.DataFrame],
    fed_events: pd.DataFrame,
    price_col: str = "Adj Close",
    normalize: bool = True,
    metric: str = "mean"
) -> pd.DataFrame:
    """
    Confronta coppie di titoli su tutti i periodi Fed e misura la
    sovraperformance come area fra i rendimenti cumulativi log,
    opzionalmente normalizzata fra -1 e +1.

    Parameters
    ----------
    stocks_data : dict
        {symbol: DataFrame} con colonne ['Date', price_col]
    fed_events : pd.DataFrame
        Colonne ['Start', 'End', 'Delta_Fed']
    price_col : str
        Colonna con i prezzi (es. 'Adj Close')
    normalize : bool, default True
        Se True, restituisce l'area normalizzata (-1 → +1)
        Se False, restituisce l'area grezza (positiva o negativa)
    metric : str, default "mean"
        Metrica di aggregazione: "mean", "median", "counts", o "percentage"
        - "mean": media delle aree
        - "median": mediana delle aree
        - "counts": numero assoluto di eventi con area positiva
        - "percentage": percentuale di eventi con area positiva

    Returns
    -------
    pd.DataFrame con colonne:
        - Per metric="mean" o "median":
          [Pair, Metric_Area_PosFed, Std_Area_PosFed,
           Metric_Area_NegFed, Std_Area_NegFed,
           N_events_PosFed, N_events_NegFed, N_events_Total]
        - Per metric="counts" o "percentage":
          [Pair, Metric_Area_PosFed, Metric_Area_NegFed,
           N_events_PosFed, N_events_NegFed, N_events_Total]
    """

    if metric not in ["mean", "median", "counts", "percentage"]:
        raise ValueError("metric deve essere 'mean', 'median', 'counts', o 'percentage'")

    pairs = list(combinations(stocks_data.keys(), 2))
    results = []

    # Etichetta per le colonne in base alla metrica
    metric_label = metric.capitalize()

    for sym1, sym2 in pairs:
        df1, df2 = stocks_data[sym1].copy(), stocks_data[sym2].copy()
        df1["Date"] = pd.to_datetime(df1["Date"])
        df2["Date"] = pd.to_datetime(df2["Date"])
        df1 = df1.set_index("Date").sort_index()
        df2 = df2.set_index("Date").sort_index()

        areas_pos, areas_neg = [], []
        pos_events = neg_events = 0

        for _, row in fed_events.iterrows():
            start, end = pd.to_datetime(row["Start"]), pd.to_datetime(row["End"])
            delta = float(row["Delta_Fed"])
            seg1 = df1.loc[start:end]
            seg2 = df2.loc[start:end]
            if len(seg1) < 2 or len(seg2) < 2:
                continue

            r1 = (seg1[price_col] / seg1.iloc[0][price_col]) * 100
            r2 = (seg2[price_col] / seg2.iloc[0][price_col]) * 100

            df = pd.DataFrame({"r1": r1, "r2": r2})
            df["spread"] = df["r1"] - df["r2"]

            # --- Inserisce i punti di incrocio per calcolo area accurata ---
            cross_points = []
            vals = df["spread"].values
            idxs = df.index.values

            for i in range(len(vals) - 1):
                y0, y1 = vals[i], vals[i + 1]
                if y0 == 0:  # spread esattamente 0
                    cross_points.append((idxs[i], df["r1"].iloc[i], df["r2"].iloc[i]))
                elif y0 * y1 < 0:  # cambio di segno ⇒ incrocio
                    frac = abs(y0) / (abs(y0 - y1))
                    t0, t1 = pd.to_datetime(idxs[i]), pd.to_datetime(idxs[i + 1])
                    t_cross = t0 + (t1 - t0) * frac
                    r1_cross = df["r1"].iloc[i] + frac * (
                        df["r1"].iloc[i + 1] - df["r1"].iloc[i]
                    )
                    r2_cross = df["r2"].iloc[i] + frac * (
                        df["r2"].iloc[i + 1] - df["r2"].iloc[i]
                    )
                    cross_points.append((t_cross, r1_cross, r2_cross))

            if cross_points:
                df_cross = pd.DataFrame(cross_points, columns=["Date", "r1", "r2"]).set_index("Date")
                df_full = pd.concat([df[["r1", "r2"]], df_cross]).sort_index()
            else:
                df_full = df[["r1", "r2"]].copy()

            df_full["spread"] = df_full["r1"] - df_full["r2"]
            spread = df_full["spread"].values

            if len(spread) < 2:
                continue

            # Calcolo aree
            area_pos = np.trapezoid(spread[spread > 0], dx=1) if np.any(spread > 0) else 0
            area_neg = np.trapezoid(-spread[spread < 0], dx=1) if np.any(spread < 0) else 0
            area_total = area_pos + area_neg

            # Normalizzazione opzionale
            if normalize and area_total > 0:
                area_value = (area_pos - area_neg) / area_total
            else:
                area_value = area_pos - area_neg

            # Salva nei gruppi
            if delta > 0:
                pos_events += 1
                areas_pos.append(area_value)
            elif delta < 0:
                neg_events += 1
                areas_neg.append(area_value)

        total_events = pos_events + neg_events
        if total_events == 0:
            continue

        # Calcola la metrica appropriata e costruisci il risultato
        result = {"Pair": f"{sym1}-{sym2}"}

        if metric == "mean":
            result[f"{metric_label}_Area_PosFed"] = np.mean(areas_pos) if areas_pos else np.nan
            result[f"Std_Area_PosFed"] = np.std(areas_pos) if areas_pos else np.nan
            result[f"{metric_label}_Area_NegFed"] = np.mean(areas_neg) if areas_neg else np.nan
            result[f"Std_Area_NegFed"] = np.std(areas_neg) if areas_neg else np.nan
        elif metric == "median":
            result[f"{metric_label}_Area_PosFed"] = np.median(areas_pos) if areas_pos else np.nan
            result[f"Std_Area_PosFed"] = np.std(areas_pos) if areas_pos else np.nan
            result[f"{metric_label}_Area_NegFed"] = np.median(areas_neg) if areas_neg else np.nan
            result[f"Std_Area_NegFed"] = np.std(areas_neg) if areas_neg else np.nan
        elif metric == "counts":
            result[f"{metric_label}_Area_PosFed"] = int(np.sum(np.array(areas_pos) > 0)) if areas_pos else 0
            result[f"{metric_label}_Area_NegFed"] = int(np.sum(np.array(areas_neg) > 0)) if areas_neg else 0
        else:  # metric == "percentage"
            result[f"{metric_label}_Area_PosFed"] = (np.sum(np.array(areas_pos) > 0) / len(areas_pos) * 100) if areas_pos else np.nan
            result[f"{metric_label}_Area_NegFed"] = (np.sum(np.array(areas_neg) > 0) / len(areas_neg) * 100) if areas_neg else np.nan

        result["N_events_PosFed"] = pos_events
        result["N_events_NegFed"] = neg_events
        result["N_events_Total"] = total_events

        results.append(result)

    return pd.DataFrame(results)



# def plot_fed_area_dominance(
#     tickers: Dict[str, pd.DataFrame],
#     event_date: str,
#     price_col: str = "Adj Close",
#     pre_days: int = 21,
#     post_days: int = 21,
#     show_dominance: bool = True,
# ):
#     symbols = list(tickers.keys())
#     if len(symbols) != 2:
#         print(f"⚠️ Error: exactly two tickers required, got {len(symbols)}.")
#         return

#     sym1, sym2 = symbols[0], symbols[1]
#     df1, df2 = tickers[sym1].copy(), tickers[sym2].copy()

#     df1["Date"] = pd.to_datetime(df1["Date"])
#     df2["Date"] = pd.to_datetime(df2["Date"])
#     df1 = df1.set_index("Date").sort_index()
#     df2 = df2.set_index("Date").sort_index()

#     event_date = pd.to_datetime(event_date)
#     start_plot = event_date - timedelta(days=pre_days)
#     end_plot = event_date + timedelta(days=post_days)

#     seg1 = df1.loc[start_plot:end_plot]
#     seg2 = df2.loc[start_plot:end_plot]
#     if len(seg1) < 2 or len(seg2) < 2:
#         print("⚠️ Insufficient data in the selected window.")
#         return

#     base1 = seg1.loc[event_date, price_col]
#     base2 = seg2.loc[event_date, price_col]

#     r1 = (seg1[price_col] / base1 - 1) * 100
#     r2 = (seg2[price_col] / base2 - 1) * 100
#     rel_days = (seg1.index - event_date).days

#     df = pd.DataFrame({"rel_days": rel_days, "r1": r1.values, "r2": r2.values})
#     df["spread"] = df["r1"] - df["r2"]

#     mask_post_event = df["rel_days"] >= 0
#     y = df.loc[mask_post_event, "spread"].values
#     area_pos = np.trapezoid(y[y > 0], dx=1) if np.any(y > 0) else 0
#     area_neg = np.trapezoid(-y[y < 0], dx=1) if np.any(y < 0) else 0
#     denom = area_pos + area_neg
#     area_norm = (area_pos - area_neg) / denom if denom > 0 else np.nan
#     dominance = area_pos / denom if denom > 0 else np.nan
#     winner = (
#         "N/A"
#         if np.isnan(area_norm)
#         else sym1
#         if area_norm > 0
#         else sym2
#         if area_norm < 0
#         else "Parity"
#     )

#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.plot(df["rel_days"], df["r1"], color="tab:blue", label=sym1, linewidth=2, zorder=3)
#     ax.plot(df["rel_days"], df["r2"], color="tab:orange", label=sym2, linewidth=2, zorder=3)

#     ax.fill_between(
#         df.loc[mask_post_event, "rel_days"],
#         df.loc[mask_post_event, "r1"],
#         df.loc[mask_post_event, "r2"],
#         where=(df.loc[mask_post_event, "spread"] > 0),
#         color="tab:blue",
#         alpha=0.25,
#         interpolate=True,
#         label=f"{sym1} outperforming area",
#     )

#     ax.fill_between(
#         df.loc[mask_post_event, "rel_days"],
#         df.loc[mask_post_event, "r1"],
#         df.loc[mask_post_event, "r2"],
#         where=(df.loc[mask_post_event, "spread"] < 0),
#         color="tab:orange",
#         alpha=0.25,
#         interpolate=True,
#         label=f"{sym2} outperforming area",
#     )

#     ax.axvline(0, color="black", linestyle="--", linewidth=1, label="Fed event")
#     ax.axhline(0, color="gray", linestyle=":", zorder=1)

#     ax.set_title(
#         f"Relative Performance Areas | {sym1} vs {sym2}\n"
#         f"Fed Event: {event_date.date()} | Analysis ±{post_days} days"
#     )
#     ax.set_xlabel("Days relative to the event")
#     ax.set_ylabel("Price change relative to event day (%)")
#     ax.grid(True, zorder=0)

#     if show_dominance:
#         ax.text(
#             0.02,
#             0.95,
#             f"Normalized area = {area_norm:+.2f}\n"
#             f"{sym1} dominance = {dominance*100:.1f}%\n"
#             f"Winner = {winner}",
#             transform=ax.transAxes,
#             fontsize=10,
#             verticalalignment="top",
#             bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"),
#             zorder=4,
#         )

#     ax.legend(loc="lower left", framealpha=0.85)
#     plt.tight_layout()
#     plt.show()



def _plot_fed_area_dominance_single(
    tickers: dict,
    event_date: str,
    delta_fed: float,
    price_col: str = "Adj Close",
    pre_days: int = 21,
    post_days: int = 21,
    show_dominance: bool = True,
):
    symbols = list(tickers.keys())
    if len(symbols) != 2:
        print(f"⚠️ Error: exactly two tickers required, got {len(symbols)}.")
        return

    sym1, sym2 = symbols[0], symbols[1]
    df1, df2 = tickers[sym1].copy(), tickers[sym2].copy()

    df1["Date"] = pd.to_datetime(df1["Date"])
    df2["Date"] = pd.to_datetime(df2["Date"])
    df1 = df1.set_index("Date").sort_index()
    df2 = df2.set_index("Date").sort_index()

    event_date = pd.to_datetime(event_date)
    start_plot = event_date - timedelta(days=pre_days)
    end_plot = event_date + timedelta(days=post_days)

    seg1 = df1.loc[start_plot:end_plot]
    seg2 = df2.loc[start_plot:end_plot]
    if len(seg1) < 2 or len(seg2) < 2:
        print("⚠️ Insufficient data in the selected window.")
        return

    base1 = seg1.loc[event_date, price_col]
    base2 = seg2.loc[event_date, price_col]

    r1 = (seg1[price_col] / base1 - 1) * 100
    r2 = (seg2[price_col] / base2 - 1) * 100
    rel_days = (seg1.index - event_date).days

    df = pd.DataFrame({"rel_days": rel_days, "r1": r1.values, "r2": r2.values})
    df["spread"] = df["r1"] - df["r2"]

    mask_post_event = df["rel_days"] >= 0
    y = df.loc[mask_post_event, "spread"].values
    area_pos = np.trapezoid(y[y > 0], dx=1) if np.any(y > 0) else 0
    area_neg = np.trapezoid(-y[y < 0], dx=1) if np.any(y < 0) else 0
    denom = area_pos + area_neg
    area_norm = (area_pos - area_neg) / denom if denom > 0 else np.nan
    dominance = area_pos / denom if denom > 0 else np.nan
    winner = (
        "N/A"
        if np.isnan(area_norm)
        else sym1
        if area_norm > 0
        else sym2
        if area_norm < 0
        else "Parity"
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        df["rel_days"],
        df["r1"],
        color="tab:blue",
        label=sym1,
        linewidth=2,
        zorder=3,
    )
    ax.plot(
        df["rel_days"],
        df["r2"],
        color="tab:orange",
        label=sym2,
        linewidth=2,
        zorder=3,
    )

    ax.fill_between(
        df.loc[mask_post_event, "rel_days"],
        df.loc[mask_post_event, "r1"],
        df.loc[mask_post_event, "r2"],
        where=(df.loc[mask_post_event, "spread"] > 0),
        color="tab:blue",
        alpha=0.25,
        interpolate=True,
        label=f"{sym1} outperforming area",
    )

    ax.fill_between(
        df.loc[mask_post_event, "rel_days"],
        df.loc[mask_post_event, "r1"],
        df.loc[mask_post_event, "r2"],
        where=(df.loc[mask_post_event, "spread"] < 0),
        color="tab:orange",
        alpha=0.25,
        interpolate=True,
        label=f"{sym2} outperforming area",
    )

    ax.axvline(0, color="black", linestyle="--", linewidth=1, label="Fed event")
    ax.axhline(0, color="gray", linestyle=":", zorder=1)

    # info sul segno dell'evento
    if delta_fed > 0:
        sign_str = "Positive"
    elif delta_fed < 0:
        sign_str = "Negative"
    else:
        sign_str = "Neutral"

    ax.set_title(
        f"Relative Performance Areas | {sym1} vs {sym2}\n"
        f"Fed Event: {event_date.date()} "
        f"({sign_str} ΔFed = {delta_fed:+.4f})"
    )
    ax.set_xlabel("Days relative to the event")
    ax.set_ylabel("Price change relative to event day (%)")
    ax.grid(True, zorder=0)

    if show_dominance:
        ax.text(
            0.02,
            0.95,
            f"Normalized area = {area_norm:+.2f}\n"
            f"{sym1} dominance = {dominance*100:.1f}%\n"
            f"Winner = {winner}",
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(facecolor="white", alpha=0.7, edgecolor="none"),
            zorder=4,
        )

    # legend in alto a sinistra
    ax.legend(loc="lower left", framealpha=0.85)
    plt.tight_layout()
    plt.show()

def plot_fed_area_dominance_events(
    tickers: dict,
    events: pd.DataFrame,
    price_col: str = "Adj Close",
    pre_days: int = 21,
    post_days: int = 21,
    top_n_pos: int = 5,
    top_n_neg: int = 5,
    use_start_as_event: bool = True,
    show_dominance: bool = True,
):
    """
    tickers: dict {symbol: df_price}
    events: DataFrame con colonne ['Start', 'End', 'Delta_Fed']
    """

    # assicuriamoci che le date siano datetime
    events = events.copy()
    events["Start"] = pd.to_datetime(events["Start"])
    events["End"] = pd.to_datetime(events["End"])

    # top positivi e negativi per Delta_Fed
    pos_events = (
        events[events["Delta_Fed"] > 0]
        .sort_values("Delta_Fed", ascending=False)
        .head(top_n_pos)
    )
    neg_events = (
        events[events["Delta_Fed"] < 0]
        .sort_values("Delta_Fed", ascending=True)
        .head(top_n_neg)
    )

    print(f"Plotting {len(pos_events)} positive and {len(neg_events)} negative events.")

    # funzione interna per scegliere la data dell'evento
    def _get_event_date(row):
        return row["Start"] if use_start_as_event else row["End"]

    # positivi
    for idx, row in pos_events.iterrows():
        event_date = _get_event_date(row)
        delta_fed = row["Delta_Fed"]
        print(f"\nPositive event {idx}: date={event_date.date()}, ΔFed={delta_fed:+.4f}")
        _plot_fed_area_dominance_single(
            tickers=tickers,
            event_date=event_date,
            delta_fed=delta_fed,
            price_col=price_col,
            pre_days=pre_days,
            post_days=post_days,
            show_dominance=show_dominance,
        )

    # negativi
    for idx, row in neg_events.iterrows():
        event_date = _get_event_date(row)
        delta_fed = row["Delta_Fed"]
        print(f"\nNegative event {idx}: date={event_date.date()}, ΔFed={delta_fed:+.4f}")
        _plot_fed_area_dominance_single(
            tickers=tickers,
            event_date=event_date,
            delta_fed=delta_fed,
            price_col=price_col,
            pre_days=pre_days,
            post_days=post_days,
            show_dominance=show_dominance,
        )






def add_winner_info(
    df: pd.DataFrame,
    pct_col: str,
    label: str = "PosFed",
) -> pd.DataFrame:
    """
    Add columns 'Winner' (ETF / Stock) and 'Fed_sign_type' (PosFed / NegFed)
    to the results dataframe.

    Parameters
    ----------
    df : DataFrame
        df_posFed or df_negFed with the percentage column.
    pct_col : str
        Name of the percentage column:
        - 'Percentage_Area_PosFed' for positive events
        - 'Percentage_Area_NegFed' for negative events
    label : str
        Label for the event type ('PosFed' or 'NegFed').

    Returns
    -------
    DataFrame
        Copy of df with additional columns.
    """
    if df.empty:
        return df.copy()

    out = df.copy()

    out["Winner"] = np.where(
        out[pct_col] > 50,
        "ETF",
        np.where(out[pct_col] < 50, "Stock", "Tie"),
    )
    out["Fed_sign_type"] = label
    return out


def plot_overall_wins(df_all: pd.DataFrame) -> None:
    """
    Overall bar chart: how many times ETF / Stock win,
    separating PosFed and NegFed events.

    Parameters
    ----------
    df_all : DataFrame
        Concatenation of df_pos and df_neg, containing at least:
        - 'Winner' (ETF / Stock / Tie)
        - 'Fed_sign_type' ('PosFed' / 'NegFed')
    """
    if df_all.empty:
        print("No results to plot.")
        return

    counts = (
        df_all.groupby(["Fed_sign_type", "Winner"])
        .size()
        .reset_index(name="count")
    )

    winners_order = ["ETF", "Stock"]
    fed_order = ["PosFed", "NegFed"]

    fig, ax = plt.subplots(figsize=(6, 4))
    width = 0.35
    x = np.arange(len(fed_order))

    for i, w in enumerate(winners_order):
        vals = []
        for f in fed_order:
            v = counts.loc[
                (counts["Fed_sign_type"] == f) & (counts["Winner"] == w),
                "count",
            ]
            vals.append(v.iloc[0] if len(v) else 0)

        ax.bar(
            x + (i - 1) * width / 1.5,
            vals,
            width / 1.5,
            label=w,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(fed_order)
    ax.set_ylabel("Number of significant pairs")
    ax.set_title("ETF vs Stock wins by Fed event sign")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_wins_by_sector(
    df_all: pd.DataFrame,
    fed_sign_type: str = "PosFed",
) -> None:
    """
    Sector-level bar chart: how many times ETF / Stock win
    for a given Fed event sign (PosFed or NegFed).

    Parameters
    ----------
    df_all : DataFrame
        Concatenation of df_pos and df_neg, with at least:
        - 'Sector'
        - 'Fed_sign_type'
        - 'Winner'
    fed_sign_type : str
        'PosFed' or 'NegFed'.
    """
    df = df_all[df_all["Fed_sign_type"] == fed_sign_type]
    if df.empty:
        print(f"No results for {fed_sign_type}.")
        return

    counts = (
        df.groupby(["Sector", "Winner"])
        .size()
        .reset_index(name="count")
    )

    sectors = sorted(counts["Sector"].unique())
    winners_order = ["ETF", "Stock"]

    fig, ax = plt.subplots(figsize=(10, 4 + len(sectors) * 0.2))

    x = np.arange(len(sectors))
    width = 0.25

    for i, w in enumerate(winners_order):
        vals = []
        for s in sectors:
            v = counts.loc[
                (counts["Sector"] == s) & (counts["Winner"] == w),
                "count",
            ]
            vals.append(v.iloc[0] if len(v) else 0)

        ax.bar(x + (i - 1) * width, vals, width, label=w)

    ax.set_xticks(x)
    ax.set_xticklabels(sectors, rotation=45, ha="right")
    ax.set_ylabel("Number of significant pairs")
    ax.set_title(f"ETF vs Stock wins by sector ({fed_sign_type})")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.show()


def _safe_get_series(df: pd.DataFrame, col: str, default=np.nan):
    """
    Return df[col] if it exists, otherwise a Series filled with `default`.
    """
    if col in df.columns:
        return df[col]
    return pd.Series([default] * len(df), index=df.index)


def build_pair_summary(df_all: pd.DataFrame) -> pd.DataFrame:
    """
    Build a detailed table for each ETF–stock pair:
    who wins, metric value, number of events, p-value.

    Parameters
    ----------
    df_all : DataFrame
        Concatenated DataFrame with:
        - 'Sector', 'ETF', 'Component'
        - 'Fed_sign_type' ('PosFed' / 'NegFed')
        - 'Winner'
        - 'Percentage_Area_PosFed' (for PosFed, if present)
        - 'Percentage_Area_NegFed' (for NegFed, if present)
        - 'N_events_PosFed', 'N_events_NegFed' (if present)
        - 'pval'

    Returns
    -------
    DataFrame
        Summary table sorted by sector, event type, winner and metric.
    """
    if df_all.empty:
        return pd.DataFrame()

    df = df_all.copy()

    # metric: percentage area depending on event type
    metric_pos = _safe_get_series(df, "Percentage_Area_PosFed")
    metric_neg = _safe_get_series(df, "Percentage_Area_NegFed")

    df["Metric"] = np.where(
        df["Fed_sign_type"] == "PosFed",
        metric_pos,
        metric_neg,
    )

    n_events_pos = _safe_get_series(df, "N_events_PosFed")
    n_events_neg = _safe_get_series(df, "N_events_NegFed")

    df["N_events"] = np.where(
        df["Fed_sign_type"] == "PosFed",
        n_events_pos,
        n_events_neg,
    )

    df_summary = df[
        [
            "Sector",
            "Fed_sign_type",
            "ETF",
            "Component",
            "Winner",
            "Metric",
            "N_events",
            "pval",
        ]
    ].sort_values(
        ["Sector", "Fed_sign_type", "Winner", "Metric"],
        ascending=[True, True, False, False],
    )

    return df_summary