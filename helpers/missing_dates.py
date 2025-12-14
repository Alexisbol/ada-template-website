import pandas as pd
import pandas_market_calendars as mcal
from pathlib import Path
from tqdm import tqdm
import shutil
import multiprocessing as mp


def _clean_and_trim_csv(args):
    csv_path, output_folder, large_gap_threshold = args
    try:
        df = pd.read_csv(csv_path)
    except Exception:
        return {"Symbol": csv_path.stem, "Start_Date": None, "End_Date": None}

    if "Date" not in df.columns:
        return {"Symbol": csv_path.stem, "Start_Date": None, "End_Date": None}

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").reset_index(drop=True)
    if len(df) < 3:
        return {"Symbol": csv_path.stem, "Start_Date": None, "End_Date": None}

    start_date = df["Date"].min().date()
    end_date = df["Date"].max().date()
    nyse = mcal.get_calendar("NYSE")
    sched = nyse.schedule(start_date=start_date, end_date=end_date)
    trading_days = sched.index.normalize()
    df["gap_days"] = df["Date"].diff().dt.days.fillna(0)
    first_gap = df["gap_days"].iloc[1]
    last_gap = (df["Date"].iloc[-1] - df["Date"].iloc[-2]).days
    start_idx, end_idx = 0, len(df)
    if first_gap > large_gap_threshold:
        start_idx = 1
    if last_gap > large_gap_threshold:
        end_idx = len(df) - 1
    cleaned_df = df.iloc[start_idx:end_idx].copy()
    cleaned_df.drop(columns=["gap_days"], inplace=True)
    output_folder.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_folder / csv_path.name, index=False)
    if cleaned_df.empty:
        return {"Symbol": csv_path.stem, "Start_Date": None, "End_Date": None}
    return {
        "Symbol": csv_path.stem,
        "Start_Date": cleaned_df["Date"].min().date(),
        "End_Date": cleaned_df["Date"].max().date(),
    }


def process_folder(input_dir: Path, output_dir: Path, large_gap_threshold: int = 200) -> pd.DataFrame:
    csv_files = sorted(input_dir.glob("*.csv"))
    args_list = [(csv_path, output_dir, large_gap_threshold) for csv_path in csv_files]
    results = []
    with mp.Pool(processes=mp.cpu_count()) as pool:
        for res in tqdm(pool.imap_unordered(_clean_and_trim_csv, args_list), total=len(args_list), ncols=90):
            results.append(res)
    return pd.DataFrame(results)


def clean_market_dates(base_path: str, input_folders: list[tuple[str, str]], meta_file: str = "symbols_valid_meta_augmented.csv", large_gap_threshold: int = 200) -> pd.DataFrame:
    base_dir = Path(base_path)
    meta_path = base_dir / meta_file
    if not meta_path.exists():
        raise FileNotFoundError(f"Metadata file not found: {meta_path}")

    all_results = []
    for input_name, output_name in input_folders:
        df_res = process_folder(base_dir / input_name, base_dir / output_name, large_gap_threshold)
        all_results.append(df_res)

    range_df = pd.concat(all_results, ignore_index=True)
    meta_df = pd.read_csv(meta_path)
    meta_df = meta_df.drop(columns=["Start_Date", "End_Date"], errors="ignore")
    merged = meta_df.merge(range_df, how="left", on="Symbol")
    merged.to_csv(meta_path, index=False)

    for input_name, _ in input_folders:
        input_dir = base_dir / input_name
        if input_dir.exists():
            shutil.rmtree(input_dir, ignore_errors=True)

    return merged