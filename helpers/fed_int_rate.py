import os
import shutil
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import kagglehub


def format_fedrate_dataset(
    base_path: str,
    kaggle_dataset: str = "natashk/effective-federal-funds-rate",
) -> pd.DataFrame:
    temp_dir = Path(base_path) / "fedrate_temp"
    temp_dir.mkdir(parents=True, exist_ok=True)

    cache_path = kagglehub.dataset_download(kaggle_dataset)

    csv_files = list(Path(cache_path).rglob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Nessun file CSV trovato nel dataset {kaggle_dataset}")

    csv_path = next((f for f in csv_files if "FRB_H15" in f.name), csv_files[0])
    df = pd.read_csv(csv_path)

    if "Time Period" not in df.columns:
        time_col = next((c for c in df.columns if "date" in c.lower()), None)
        if time_col:
            df = df.rename(columns={time_col: "Time Period"})
        else:
            raise ValueError("Expected column 'Time Period' not found in dataset")

    df["Date"] = (
        df["Time Period"]
        .astype(str)
        .str.strip()
        .str.replace(" 00:00:00", "", regex=False)
        .apply(
            lambda x: f"{int(x.split('-')[1])}/{int(x.split('-')[2])}/{x.split('-')[0]}"
            if isinstance(x, str) and "-" in x
            else x
        )
    )

    rate_col = next(
        (c for c in df.columns if "RIFSPFF" in c or "FEDFUNDS" in c.upper()), None
    )
    
    df = df.rename(columns={rate_col: "Fed_rate"})

    df = df[["Date", "Fed_rate"]].dropna()

    output_path = temp_dir / "federal-funds-rate.csv"
    df.to_csv(output_path, index=False)

    result_df = df.copy()

    shutil.rmtree(temp_dir, ignore_errors=True)

    return result_df


def merge_with_fedrate(
    base_path: str,
    input_folder: str,
    output_folder: str,
    fed_df: pd.DataFrame,
) -> pd.DataFrame:
    base_dir = Path(base_path)
    input_dir = base_dir / input_folder
    output_dir = base_dir / output_folder
    output_dir.mkdir(parents=True, exist_ok=True)

    fed_df = fed_df.copy()
    fed_df["Date"] = pd.to_datetime(fed_df["Date"], errors="coerce")

    rate_col_candidates = [c for c in fed_df.columns if "rate" in c.lower() or "RIFSPFF" in c]
   
    rate_col = rate_col_candidates[0]
    if rate_col != "Fed_rate":
        fed_df = fed_df.rename(columns={rate_col: "Fed_rate"})

    csv_files = list(input_dir.glob("*.csv"))
    results = []

    for file_path in tqdm(csv_files, desc=f"Merging {input_folder}", ncols=90):
        try:
            df_asset = pd.read_csv(file_path)
            if "Date" not in df_asset.columns:
                raise KeyError(f"Missing 'Date' column in {file_path.name}")

            df_asset["Date"] = pd.to_datetime(df_asset["Date"], errors="coerce")
            merged = pd.merge(fed_df, df_asset, on="Date", how="inner")
            merged["Date"] = merged["Date"].dt.strftime("%-m/%-d/%Y")

            output_path = output_dir / file_path.name
            merged.to_csv(output_path, index=False)
            results.append((file_path.name, len(merged)))
        except Exception as e:
            results.append((file_path.name, f"Error: {e}"))

    
   