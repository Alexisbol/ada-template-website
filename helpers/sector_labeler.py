import os
import pandas as pd
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
import kagglehub
import glob
import multiprocessing
from tqdm import tqdm
from contextlib import suppress
import shutil
import matplotlib.pyplot as plt


def label_stock_sectors_1(df_symbols: pd.DataFrame) -> pd.DataFrame:
    
    tickers = sorted(df_symbols["Symbol"].dropna().unique().tolist())
    def get_ticker_sector(ticker):
        with suppress(Exception):
            info = yf.Ticker(ticker).info
            return {"Ticker": ticker, "Sector": info.get("sector", "Unknown")}
        return {"Ticker": ticker, "Sector": "Unknown"}
    results = []
    num_workers = multiprocessing.cpu_count()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(get_ticker_sector, t) for t in tickers]
        for f in tqdm(as_completed(futures), total=len(futures), desc="Fetching stock sectors"):
            results.append(f.result())
    return pd.DataFrame(results)


def label_stock_sectors_2(df_symbols: pd.DataFrame) -> pd.DataFrame:
    kaggle_dataset = "mariyamalshatta/trade-and-ahead-stock-data"
    ticker_col = "Ticker Symbol"
    sector_col = "GICS Sector"
    local_temp_path = os.path.join("data", "kaggle_temp")
    os.makedirs(local_temp_path, exist_ok=True)
    cache_path = kagglehub.dataset_download(kaggle_dataset)

    for file in glob.glob(os.path.join(cache_path, "**", "*"), recursive=True):
        if os.path.isfile(file):
            dest = os.path.join(local_temp_path, os.path.basename(file))
            with suppress(Exception):
                shutil.copy(file, dest)

    csv_files = glob.glob(os.path.join(local_temp_path, "**", "*.csv"), recursive=True)
    if not csv_files:
        raise FileNotFoundError(f"Nessun CSV trovato in {local_temp_path}")

    df = pd.read_csv(csv_files[0], low_memory=False)
    if ticker_col not in df.columns or sector_col not in df.columns:
        raise KeyError(f"Mancano le colonne: {ticker_col}, {sector_col}")

    df = df.rename(columns={ticker_col: "Symbol", sector_col: "Sector_GICS"})
    df = (
        df[["Symbol", "Sector_GICS"]]
        .dropna()
        .query("Sector_GICS != 'N/A'")
        .drop_duplicates(subset=["Symbol"], keep="first")
    )

    if "Symbol" not in df_symbols.columns:
        raise KeyError("Il DataFrame df_symbols deve avere la colonna 'Symbol'.")

    df = df.merge(df_symbols[["Symbol"]].drop_duplicates(), on="Symbol", how="inner")

    with suppress(Exception):
        shutil.rmtree(local_temp_path)

    return df


def label_etf_sectors(df_symbols: pd.DataFrame) -> pd.DataFrame:
    if "Symbol" not in df_symbols.columns or "ETF" not in df_symbols.columns:
        raise KeyError("Il DataFrame deve contenere le colonne 'Symbol' e 'ETF'.")
    tickers = df_symbols.loc[df_symbols["ETF"] == "Y", "Symbol"].dropna().unique().tolist()
    def map_sector(raw: str) -> str:
        if not isinstance(raw, str) or raw.strip() == "":
            return "Unknown"
        s = raw.lower()
        mapping = {
            "tech": "Technology",
            "info": "Technology",
            "internet": "Technology",
            "financ": "Financial Services",
            "bank": "Financial Services",
            "dividend": "Financial Services",
            "health": "Healthcare",
            "pharma": "Healthcare",
            "bio": "Healthcare",
            "indust": "Industrials",
            "aero": "Industrials",
            "defense": "Industrials",
            "energy": "Energy",
            "oil": "Energy",
            "gas": "Energy",
            "fuel": "Energy",
            "utility": "Utilities",
            "real": "Real Estate",
            "reit": "Real Estate",
            "property": "Real Estate",
            "consumer": "Consumer Cyclical",
            "retail": "Consumer Cyclical",
            "cyclic": "Consumer Cyclical",
            "staple": "Consumer Defensive",
            "defens": "Consumer Defensive",
            "food": "Consumer Defensive",
            "basic": "Basic Materials",
            "mater": "Basic Materials",
            "metals": "Basic Materials",
            "communicat": "Communication Services",
            "telecom": "Communication Services",
            "media": "Communication Services",
        }
        for k, v in mapping.items():
            if k in s:
                return v
        return "Unknown"
    def get_etf_sector(symbol: str):
        with suppress(Exception):
            info = yf.Ticker(symbol).info
            raw = (
                info.get("sector")
                or info.get("category")
                or info.get("quoteType")
                or "Unknown"
            )
            return {"Symbol": symbol, "Sector": map_sector(raw)}
        return {"Symbol": symbol, "Sector": "Unknown"}
    results = []
    num_workers = multiprocessing.cpu_count()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(get_etf_sector, t) for t in tickers]
        for f in tqdm(as_completed(futures), total=len(futures), desc="Fetching ETF sectors"):
            results.append(f.result())
    df_map = pd.DataFrame(results).drop_duplicates(subset=["Symbol"], keep="first")
    return df_map



def combine_and_map_sectors(
    df_symbols: pd.DataFrame,
    df_sector_map_1: pd.DataFrame,
    df_sector_map_2: pd.DataFrame,
    df_etf_map: pd.DataFrame,
    output_path: str = "data/symbols_valid_meta_augmented.csv",
) -> pd.DataFrame:
    df_meta = df_symbols.copy()

    df_yf = df_sector_map_1.rename(columns={"Ticker": "Symbol", "Sector": "Sector_YF"})[
        ["Symbol", "Sector_YF"]
    ].drop_duplicates(subset=["Symbol"])

    df_gics = df_sector_map_2.rename(
        columns={"Symbol": "Symbol", "Sector_GICS": "Sector_GICS"}
    )[["Symbol", "Sector_GICS"]].drop_duplicates(subset=["Symbol"])

    df_etf = df_etf_map.rename(columns={"Sector": "Sector_Curated"})[
        ["Symbol", "Sector_Curated"]
    ].drop_duplicates(subset=["Symbol"])

    df_final = (
        df_meta.merge(df_gics, on="Symbol", how="left")
        .merge(df_etf, on="Symbol", how="left")
        .merge(df_yf, on="Symbol", how="left")
    )

    df_final["Raw_Final_Sector"] = df_final["Sector_YF"].combine_first(
        df_final["Sector_Curated"].combine_first(df_final["Sector_GICS"])
    )
    df_final["Raw_Final_Sector"] = df_final["Raw_Final_Sector"].fillna("Unknown")

    standardization_map = {
        "Industrials": "Industrials",
        "Healthcare": "Healthcare",
        "Health Care": "Healthcare",
        "Financial Services": "Financial Services",
        "Financials": "Financial Services",
        "Technology": "Technology",
        "Information Technology": "Technology",
        "Real Estate": "Real Estate",
        "Basic Materials": "Basic Materials",
        "Consumer Defensive": "Consumer Defensive",
        "Consumer Staples": "Consumer Defensive",
        "Utilities": "Utilities",
        "Energy": "Energy",
        "Communication Services": "Communication Services",
    }

    def standardize_sector(sector):
        if pd.isna(sector) or sector == "Unknown":
            return "Unknown"
        cleaned = sector.strip().title()
        return standardization_map.get(cleaned, cleaned)

    df_final["Sector"] = df_final["Raw_Final_Sector"].apply(standardize_sector)
    df_output = df_final.drop(
        columns=["Sector_YF", "Sector_Curated", "Sector_GICS", "Raw_Final_Sector"],
        errors="ignore",
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_output.to_csv(output_path, index=False)

    return df_output

def plot_sector_distribution(df: pd.DataFrame):
    sector_counts = df["Sector"].value_counts()
    sector_counts_plot = sector_counts.drop("Unknown", errors="ignore")

    plt.figure(figsize=(14, 8))
    sector_counts_plot.plot(kind="bar", color="darkcyan", edgecolor="black")

    plt.title(
        "Ticker Distribution by Sector (11 Standardized GICS Categories)",
        fontsize=16,
    )
    plt.xlabel("Sector", fontsize=14)
    plt.ylabel("Number of Tickers", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    for index, value in enumerate(sector_counts_plot):
        plt.text(index, value + 0.5, str(value), ha="center", va="bottom")

    plt.show()