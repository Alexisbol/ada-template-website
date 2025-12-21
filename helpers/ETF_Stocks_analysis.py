import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def load_financial_data(
    symbol: str,
    folder: str,
    date_col: str = "Date",
    required_cols: List[str] = ["Date", "Close", "Fed_rate"]
) -> Optional[pd.DataFrame]:
    file_path = Path(folder) / f"{symbol}.csv"
    if not file_path.exists():
        return None
    df = pd.read_csv(file_path, parse_dates=[date_col])
    return df.dropna(subset=required_cols)


def aggregate_stock_components(
    stock_symbols: List[str],
    folder: str
) -> pd.DataFrame:
    stock_dfs = [load_financial_data(sym, folder) for sym in stock_symbols]
    stock_dfs = [df for df in stock_dfs if df is not None]
    
    if not stock_dfs:
        raise RuntimeError("No stock data files available")
    
    aggregated = (
        pd.concat(stock_dfs)
        .groupby("Date", as_index=False)
        .agg({"Close": "mean", "Fed_rate": "last"})
        .dropna()
        .sort_values("Date")
    )
    return aggregated


def identify_fed_events(
    df: pd.DataFrame,
    threshold: float = 0.5,
    lookback_window: int = 21
) -> pd.DataFrame:
    rolling_avg = df['Fed_rate'].rolling(
        window=lookback_window, 
        min_periods=lookback_window
    ).mean()
    avg_prev_month = rolling_avg.shift(lookback_window)
    df['dFed'] = (df['Fed_rate'] - avg_prev_month).round(2)
    
    big_moves = df[df["dFed"].abs() >= threshold].dropna()
    return big_moves


def filter_stable_events(
    df: pd.DataFrame,
    events: pd.DataFrame,
    stability_window: int = 30,
    stability_range: float = 0.25
) -> pd.DataFrame:
    stable_events = []
    
    for idx, row in events.iterrows():
        end_idx = idx + stability_window
        if end_idx >= len(df):
            continue
        
        window = df.iloc[idx:end_idx]
        rate_range = window["Fed_rate"].max() - window["Fed_rate"].min()
        
        if rate_range < stability_range:
            stable_events.append(row)
    
    if not stable_events:
        return pd.DataFrame()
    
    return pd.DataFrame(stable_events).sort_values("Date")


def remove_overlapping_events(
    events: pd.DataFrame,
    forward_window: int = 30
) -> pd.DataFrame:
    cleaned = []
    last_end = pd.Timestamp.min
    
    for _, row in events.iterrows():
        if row["Date"] >= last_end:
            cleaned.append(row)
            last_end = row["Date"] + pd.Timedelta(days=forward_window)
    
    return pd.DataFrame(cleaned)


def balance_positive_negative_events(
    events: pd.DataFrame,
    require_strict: bool = False
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    pos_events = events[events["dFed"] > 0]
    neg_events = events[events["dFed"] < 0]
    
    num_to_use = min(len(pos_events), len(neg_events))
    
    if num_to_use == 0:
        if require_strict:
            raise RuntimeError("Not enough events for balanced comparison")
        return pd.DataFrame(), pd.DataFrame()
    
    final_pos = pos_events.nlargest(num_to_use, "dFed")
    final_neg = neg_events.nsmallest(num_to_use, "dFed")
    
    return final_pos, final_neg


def calculate_normalized_returns(
    df: pd.DataFrame,
    event_date: pd.Timestamp,
    days_forward: int,
    weeks: List[int],
    dFed: Optional[float] = None,
    normalize_by_dFed: bool = False
) -> List[Tuple[int, float]]:
    slice_df = df[
        (df["Date"] >= event_date) & 
        (df["Date"] <= event_date + pd.Timedelta(days=days_forward))
    ].copy()
    
    if slice_df.empty or len(slice_df) < 2:
        return []
    
    initial_close = slice_df['Close'].iloc[0]
    if initial_close == 0:
        return []
    
    slice_df["Δd"] = (slice_df["Date"] - event_date).dt.days
    slice_df["Norm"] = slice_df["Close"] / initial_close * 100
    
    results = []
    for w in weeks:
        if w == 0:
            ret = 0.0
        elif w > slice_df["Δd"].max():
            continue
        else:
            try:
                idx = (slice_df["Δd"] - w).abs().idxmin()
                ret = slice_df.loc[idx, "Norm"] - 100
            except KeyError:
                continue
        # Optionally normalize the return by the magnitude of the Fed move
        if normalize_by_dFed and dFed is not None:
            try:
                abs_d = abs(float(dFed))
            except Exception:
                abs_d = 0.0

            if abs_d > 0:
                ret = ret / abs_d
            else:
                # keep as NaN-like marker if dFed is zero
                ret = float('nan')

        results.append((w, ret))
    
    return results


def compute_stock_vs_etf_ratio(
    etf_return: float,
    stock_return: float,
    week: int
) -> float:
    if week == 0:
        return 1.0
    
    sign = 1 if stock_return >= etf_return else -1
    abs_etf = abs(etf_return)
    abs_stock = abs(stock_return)
    
    bigger = max(abs_etf, abs_stock)
    smaller = min(abs_etf, abs_stock)
    
    epsilon = 1e-9
    magnitude = bigger / (smaller + epsilon)
    
    ratio = sign * magnitude
    return ratio if np.isfinite(ratio) else sign


def analyze_fed_rate_reaction(
    etf_symbol: str,
    stock_map: Dict[str, List[str]],
    etf_folder: str = "data/etfs+fedrate+nmv",
    stock_folder: str = "data/stocks+fedrate+nmv",
    days_forward: int = 30,
    fed_event_threshold: float = 0.5,
    fed_stable_window: int = 30,
    fed_stability_range: float = 0.25,
    require_strict: bool = False,
    summary_only: bool = False,
    normalize_by_dFed: bool = True
) -> Optional[pd.DataFrame]:
    
    if etf_symbol not in stock_map:
        raise ValueError(f"{etf_symbol} not found in stock map")
    
    etf_df = load_financial_data(etf_symbol, etf_folder)
    if etf_df is None:
        raise RuntimeError(f"Missing file for {etf_symbol}")
    
    stocks_df = aggregate_stock_components(stock_map[etf_symbol], stock_folder)
    
    big_moves = identify_fed_events(etf_df, fed_event_threshold)
    stable_df = filter_stable_events(
        etf_df, big_moves, fed_stable_window, fed_stability_range
    )
    
    if stable_df.empty:
        print(f"No stable events found for {etf_symbol}")
        return None
    
    clean_df = remove_overlapping_events(stable_df, days_forward)
    
    pos_events, neg_events = balance_positive_negative_events(
        clean_df, require_strict
    )
    
    if pos_events.empty or neg_events.empty:
        print(f"Cannot create balanced comparison for {etf_symbol}")
        return None
    
    events = pd.concat([pos_events, neg_events]).sort_values("Date")
    print(f"{etf_symbol}: {len(pos_events)} positive + {len(neg_events)} negative events")
    
    weeks = [0] + list(range(7, days_forward + 1, 7))
    rows = []
    
    for _, ev in events.iterrows():
        event_date = ev["Date"]
        bucket = "+ΔFed" if ev["dFed"] > 0 else "-ΔFed"
        
        # Calculate returns; by default normalize per 1% ΔFed so comparisons
        # account for magnitude of the policy move.
        etf_returns = calculate_normalized_returns(
            etf_df, event_date, days_forward, weeks,
            dFed=ev.get('dFed', None),
            normalize_by_dFed=normalize_by_dFed
        )
        stock_returns = calculate_normalized_returns(
            stocks_df, event_date, days_forward, weeks,
            dFed=ev.get('dFed', None),
            normalize_by_dFed=normalize_by_dFed
        )
        
        if not etf_returns or not stock_returns:
            continue
        
        etf_dict = dict(etf_returns)
        stock_dict = dict(stock_returns)
        
        for w in weeks:
            if w not in etf_dict or w not in stock_dict:
                continue
            
            e_ret = etf_dict[w]
            s_ret = stock_dict[w]
            ratio = compute_stock_vs_etf_ratio(e_ret, s_ret, w)
            
            rows.append({
                'ETF': etf_symbol,
                'bucket': bucket,
                'week': w,
                'dFed': ev['dFed'],
                'etf_avg_pct': e_ret,
                'stocks_avg_pct': s_ret,
                'stock_vs_etf_ratio': ratio
            })
    
    if not rows:
        return None
    
    result = pd.DataFrame(rows)
    
    if summary_only:
        summary_df = result.groupby(['bucket', 'week']).agg(
            median_stock_vs_etf_ratio=('stock_vs_etf_ratio', 'median'),
            event_count=('dFed', 'size')
        ).reset_index()
        return summary_df
    
    return result


def analyze_sector_etfs(
    sector_name: str,
    etfs_dict: Dict[str, List[str]],
    stock_map: Dict[str, List[str]],
    etf_folder: str = "data/etfs+fedrate+nmv",
    stock_folder: str = "data/stocks+fedrate+nmv",
    days_forward: int = 35,
    fed_event_threshold: float = 0.30,
    fed_stable_window: int = 35,
    fed_stability_range: float = 0.25
) -> Optional[pd.DataFrame]:
    
    sector_results = []
    
    for etf_symbol in etfs_dict.keys():
        try:
            summary_df = analyze_fed_rate_reaction(
                etf_symbol=etf_symbol,
                stock_map=stock_map,
                etf_folder=etf_folder,
                stock_folder=stock_folder,
                days_forward=days_forward,
                fed_event_threshold=fed_event_threshold,
                fed_stable_window=fed_stable_window,
                fed_stability_range=fed_stability_range,
                require_strict=False,
                summary_only=True
            )
            
            if summary_df is not None and not summary_df.empty:
                sector_results.append(summary_df)
                
        except Exception as e:
            print(f"Error processing {etf_symbol}: {e}")
            continue
    
    if not sector_results:
        return None
    
    combined = pd.concat(sector_results, ignore_index=True)
    return combined


def aggregate_sector_summary(
    sector_summaries: pd.DataFrame,
    sector_name: str
) -> pd.DataFrame:
    
    aggregated = sector_summaries.groupby(['bucket', 'week']).agg(
        sector_median_of_medians=('median_stock_vs_etf_ratio', 'median'),
        etfs_in_sample=('event_count', 'size')
    ).reset_index()
    
    aggregated['sector'] = sector_name
    return aggregated


def analyze_all_sectors(
    sector_etf_map: Dict[str, Dict[str, List[str]]],
    stock_map: Dict[str, List[str]],
    etf_folder: str = "data/etfs+fedrate+nmv",
    stock_folder: str = "data/stocks+fedrate+nmv",
    days_forward: int = 35,
    fed_event_threshold: float = 0.30,
    fed_stable_window: int = 35,
    fed_stability_range: float = 0.25
) -> Dict[str, pd.DataFrame]:
    
    sector_summaries = {}
    
    for sector_name, etfs_dict in sector_etf_map.items():
        print(f"\nAnalyzing sector: {sector_name.upper()}")
        
        combined_summaries = analyze_sector_etfs(
            sector_name=sector_name,
            etfs_dict=etfs_dict,
            stock_map=stock_map,
            etf_folder=etf_folder,
            stock_folder=stock_folder,
            days_forward=days_forward,
            fed_event_threshold=fed_event_threshold,
            fed_stable_window=fed_stable_window,
            fed_stability_range=fed_stability_range
        )
        
        if combined_summaries is None:
            print(f"No valid results for sector {sector_name}")
            continue
        
        final_summary = aggregate_sector_summary(combined_summaries, sector_name)
        sector_summaries[sector_name] = final_summary
    
    return sector_summaries


def convert_ratio_to_performance_pct(ratio: float) -> float:
    if abs(ratio) < 1:
        return 0.0
    return (abs(ratio) - 1) * 100 * np.sign(ratio)


def prepare_plotting_data(
    sector_summaries: Dict[str, pd.DataFrame]
) -> pd.DataFrame:
    
    if not sector_summaries:
        raise ValueError("Empty sector summaries dictionary")
    
    full_df = pd.concat(sector_summaries.values(), ignore_index=True)
    full_df['performance_pct'] = full_df['sector_median_of_medians'].apply(
        convert_ratio_to_performance_pct
    )
    
    return full_df

def plot_sector_reactions(
    data: pd.DataFrame,
    figsize: Tuple[int, int] = (20, 16),
    color_map: Optional[Dict[str, str]] = None,
    show_average: bool = True
):
    
    
    sectors = sorted(data['sector'].unique())
    
    if color_map is None:
        base_colors = [
            "#0077FF",  # blu brillante
            "#00CC44",  # verde acceso
            "#FF3333",  # rosso acceso
            "#FFAA00",  # arancio
            "#9933FF",  # viola intenso
        ]

        color_map = {
            sector: base_colors[i % len(base_colors)]
            for i, sector in enumerate(sectors)
        }
    
    weeks = sorted(data['week'].unique())
    week_labels = [f'Week {i//7}' if i > 0 else 'Day 0' for i in weeks]
    
    plt.style.use('dark_background')
    
    if show_average:
        fig, axes = plt.subplots(2, 2, figsize=figsize, sharey=True)
        axes = axes.flatten()
    else:
        fig, axes = plt.subplots(
            1, 2, figsize=(figsize[0], figsize[1]//2), sharey=True
        )
    
    fig.suptitle(
        'Sector Median Reaction to Fed Rate Changes',
        fontsize=22,
        y=0.98 if not show_average else 0.95
    )
    
    df_pos = data[data['bucket'] == '+ΔFed']
    df_neg = data[data['bucket'] == '-ΔFed']
    
    ax = axes[0]
    ax.set_title(
        'Reaction to Rate Increase (+ΔFed) by Sector', fontsize=16
    )
    for sector in sectors:
        sector_data = df_pos[df_pos['sector'] == sector]
        if not sector_data.empty:
            ax.plot(
                sector_data['week'],
                sector_data['performance_pct'],
                marker='o',
                linestyle='-',
                label=sector,
                color=color_map[sector],
                linewidth=2.5
            )
    ax.axhline(0, color='gray', linestyle='--', linewidth=1.5)
    ax.set_ylabel('Median Stock Outperformance (%)', fontsize=12)
    ax.legend(title='Sector', fontsize=9, loc='best')
    ax.grid(True, alpha=0.2)
    ax.set_xticks(weeks)
    ax.set_xticklabels(week_labels)
    
    ax = axes[1]
    ax.set_title('Reaction to Rate Cut (-ΔFed) by Sector', fontsize=16)
    for sector in sectors:
        sector_data = df_neg[df_neg['sector'] == sector]
        if not sector_data.empty:
            ax.plot(
                sector_data['week'],
                sector_data['performance_pct'],
                marker='o',
                linestyle='-',
                label=sector,
                color=color_map[sector],
                linewidth=2.5
            )
    ax.axhline(0, color='gray', linestyle='--', linewidth=1.5)
    ax.legend(title='Sector', fontsize=9, loc='best')
    ax.grid(True, alpha=0.2)
    ax.set_xticks(weeks)
    ax.set_xticklabels(week_labels)
    
    if show_average:
        ax = axes[2]
        avg_pos = df_pos.groupby('week')['performance_pct'].mean()
        ax.plot(
            avg_pos.index,
            avg_pos.values,
            marker='o',
            linestyle='-',
            color="#dfdfdf",
            linewidth=3,
            label='Cross-Sector Average'
        )
        ax.axhline(0, color='gray', linestyle='--', linewidth=1.5)
        ax.set_title('Average Sector Reaction to +ΔFed', fontsize=16)
        ax.set_xlabel('Weeks After Event', fontsize=12)
        ax.set_ylabel('Median Stock Outperformance (%)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.2)
        ax.set_xticks(weeks)
        ax.set_xticklabels(week_labels)
        
        ax = axes[3]
        avg_neg = df_neg.groupby('week')['performance_pct'].mean()
        ax.plot(
            avg_neg.index,
            avg_neg.values,
            marker='o',
            linestyle='-',
            color="#dfdfdf",
            linewidth=3,
            label='Cross-Sector Average'
        )
        ax.axhline(0, color='gray', linestyle='--', linewidth=1.5)
        ax.set_title('Average Sector Reaction to -ΔFed', fontsize=16)
        ax.set_xlabel('Weeks After Event', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.2)
        ax.set_xticks(weeks)
        ax.set_xticklabels(week_labels)
    
    plt.tight_layout(
        rect=[0, 0.03, 1, 0.94] if show_average else [0, 0.03, 1, 0.96]
    )
    plt.show()

def plot_chart_explanation(
    weeks: List[int],
    figsize: Tuple[int, int] = (16, 10)
):
    
    plt.style.use('dark_background')
    fig, (ax_main, ax_example) = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle('How to Read the Performance Charts', fontsize=20, y=0.98)
    
    week_labels = [f'Week {i//7}' if i > 0 else 'Day 0' for i in weeks]
    
    ax_main.axhspan(0, 50, alpha=0.3, color='green', label='Stocks Outperform ETF')
    ax_main.axhspan(-50, 0, alpha=0.3, color='red', label='ETF Outperforms Stocks')
    
    ax_main.axhline(0, color='white', linestyle='-', linewidth=2, 
                    label='Baseline (Equal Performance)')
    
    ax_main.annotate('STOCKS WIN\n(Higher returns than ETF)', 
                     xy=(weeks[-1]//2, 25), fontsize=14, ha='center',
                     color='lightgreen', weight='bold')
    
    ax_main.annotate('ETF WINS\n(Higher returns than stocks)', 
                     xy=(weeks[-1]//2, -25), fontsize=14, ha='center',
                     color='lightcoral', weight='bold')
    
    start_marker_x = weeks[0]
    ax_main.plot(start_marker_x, 0, 'o', markersize=15, color='yellow', 
                 zorder=5, label='Fed Rate Change Event')
    ax_main.annotate('Starting Point:\nFed Rate Change Day', 
                     xy=(start_marker_x, 0), xytext=(start_marker_x + weeks[-1]*0.15, 15),
                     fontsize=11, color='yellow',
                     arrowprops=dict(arrowstyle='->', color='yellow', lw=2))
    
    ax_main.set_ylim(-50, 50)
    ax_main.set_xlim(weeks[0] - 1, weeks[-1] + 1)
    ax_main.set_xlabel('Time After Fed Rate Event', fontsize=13)
    ax_main.set_ylabel('Stock vs ETF Performance (%)', fontsize=13)
    ax_main.set_xticks(weeks)
    ax_main.set_xticklabels(week_labels)
    ax_main.grid(True, alpha=0.3, linestyle='--')
    ax_main.legend(loc='upper left', fontsize=10)
    ax_main.set_title('Chart Regions', fontsize=14, pad=10)
    
    example_weeks = np.array(weeks)
    example_performance = np.array([0, 5, 12, 18, 25])[:len(weeks)]
    
    ax_example.axhline(0, color='white', linestyle='--', linewidth=1, alpha=0.5)
    ax_example.plot(example_weeks, example_performance, 'o-', 
                    color='cyan', linewidth=3, markersize=10, label='Example Trajectory')
    
    for i, (week, perf) in enumerate(zip(example_weeks, example_performance)):
        if week == 0:
            label_text = f'{perf:.0f}%\n(Baseline)'
        else:
            label_text = f'{perf:.0f}%'
        
        ax_example.annotate(label_text, xy=(week, perf), 
                           xytext=(0, 15), textcoords='offset points',
                           fontsize=10, ha='center', color='cyan',
                           bbox=dict(boxstyle='round,pad=0.3', 
                                   facecolor='black', alpha=0.7))
    
    if len(example_weeks) > 1:
        mid_week = example_weeks[len(example_weeks)//2]
        mid_perf = example_performance[len(example_weeks)//2]
        
        ax_example.annotate(
            f'Interpretation:\nStocks have gained\n{mid_perf:.0f}% MORE than ETF\nup to this point',
            xy=(mid_week, mid_perf),
            xytext=(mid_week + weeks[-1]*0.3, mid_perf - 10),
            fontsize=11, color='lightgreen',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='darkgreen', alpha=0.7),
            arrowprops=dict(arrowstyle='->', color='lightgreen', lw=2)
        )
    
    ax_example.set_ylim(-10, 35)
    ax_example.set_xlim(weeks[0] - 1, weeks[-1] + 1)
    ax_example.set_xlabel('Time After Event', fontsize=13)
    ax_example.set_ylabel('Cumulative Outperformance (%)', fontsize=13)
    ax_example.set_xticks(weeks)
    ax_example.set_xticklabels(week_labels)
    ax_example.grid(True, alpha=0.3, linestyle='--')
    ax_example.set_title('Example Reading', fontsize=14, pad=10)
   
    plt.tight_layout(rect=[0, 0.12, 1, 0.96])
    plt.show()


def plot_absolute_returns(
    data: pd.DataFrame,
    figsize: Tuple[int, int] = (18, 8)
):
    
    weeks = sorted(data['week'].unique())
    week_labels = [f'Week {i//7}' if i > 0 else 'Day 0' for i in weeks]
    
    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle(
        'Absolute Returns: ETF vs Stocks (Overall Market Context)',
        fontsize=18,
        y=0.98
    )
    
    df_pos = data[data['bucket'] == '+ΔFed']
    df_neg = data[data['bucket'] == '-ΔFed']
    
    ax = ax1
    ax.set_title('During Rate Increases (+ΔFed)', fontsize=15, pad=10)
    
    avg_etf_pos = df_pos.groupby('week')['etf_avg_pct'].mean()
    avg_stock_pos = df_pos.groupby('week')['stocks_avg_pct'].mean()
    
    ax.plot(avg_etf_pos.index, avg_etf_pos.values, 
            marker='o', linestyle='-', color='#FF6B6B', 
            linewidth=3, markersize=8, label='ETF Average Return')
    ax.plot(avg_stock_pos.index, avg_stock_pos.values, 
            marker='s', linestyle='-', color='#4ECDC4', 
            linewidth=3, markersize=8, label='Stocks Average Return')
    
    ax.axhline(0, color='white', linestyle='--', linewidth=1.5, alpha=0.5)
    
    ax.fill_between(avg_etf_pos.index, 0, avg_etf_pos.values,
                    alpha=0.2, color='#FF6B6B')
    ax.fill_between(avg_stock_pos.index, 0, avg_stock_pos.values,
                    alpha=0.2, color='#4ECDC4')

    ax.set_xlabel('Time After Event', fontsize=12)
    ax.set_ylabel('Cumulative Return (%)', fontsize=12)
    ax.legend(loc='best', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xticks(weeks)
    ax.set_xticklabels(week_labels)
    
    if avg_etf_pos.mean() < 0:
        ax.annotate('⚠️ Market declining during\nrate increases', 
                   xy=(weeks[-1]//2, min(avg_etf_pos.min(), avg_stock_pos.min()) - 2),
                   fontsize=10, ha='center', color='#FF6B6B',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7))
    
    ax = ax2
    ax.set_title('During Rate Cuts (-ΔFed)', fontsize=15, pad=10)
    
    avg_etf_neg = df_neg.groupby('week')['etf_avg_pct'].mean()
    avg_stock_neg = df_neg.groupby('week')['stocks_avg_pct'].mean()
    
    ax.plot(avg_etf_neg.index, avg_etf_neg.values, 
            marker='o', linestyle='-', color='#FF6B6B', 
            linewidth=3, markersize=8, label='ETF Average Return')
    ax.plot(avg_stock_neg.index, avg_stock_neg.values, 
            marker='s', linestyle='-', color='#4ECDC4', 
            linewidth=3, markersize=8, label='Stocks Average Return')
    
    ax.axhline(0, color='white', linestyle='--', linewidth=1.5, alpha=0.5)
    ax.fill_between(avg_etf_neg.index, 0, avg_etf_neg.values, 
                     alpha=0.2, color='#FF6B6B')
    ax.fill_between(avg_stock_neg.index, 0, avg_stock_neg.values, 
                     alpha=0.2, color='#4ECDC4')
    
    ax.set_xlabel('Time After Event', fontsize=12)
    ax.set_ylabel('Cumulative Return (%)', fontsize=12)
    ax.legend(loc='best', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xticks(weeks)
    ax.set_xticklabels(week_labels)
    
    if avg_etf_neg.mean() > 0:
        ax.annotate('✅ Market growing during\nrate cuts', 
                   xy=(weeks[-1]//2, max(avg_etf_neg.max(), avg_stock_neg.max()) + 2),
                   fontsize=10, ha='center', color='#4ECDC4',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='black', alpha=0.7))
    
    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.show()
    
   