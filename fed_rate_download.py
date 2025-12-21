import pandas as pd

def download_fed_rate():
    # URL for the Daily Federal Funds Rate (DFF)
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DFF"
    
    print("Downloading data from FRED...")
    
    try:
        df = pd.read_csv(url)
        # Debug: Print columns to verify what we received
        print(f"Columns found: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    # FRED usually uses 'observation_date', but we'll check just in case
    date_col = 'observation_date' if 'observation_date' in df.columns else 'DATE'

    # Convert the date column to datetime objects
    df[date_col] = pd.to_datetime(df[date_col])

    # Filter data: Start from 1962-01-01
    df = df[df[date_col] >= '1962-01-01']

    # Sort Descending (Newest date first)
    df = df.sort_values(by=date_col, ascending=False)

    # Rename columns to match your specific format
    # Map the detected date column to 'Time Period' and 'DFF' to 'RIFSPFF_N.D'
    df = df.rename(columns={date_col: 'Time Period', 'DFF': 'RIFSPFF_N.D'})

    # Save to CSV
    filename = 'fed_rate_1962_today.csv'
    df.to_csv(filename, index=False)

    print(f"Success! Data saved to '{filename}'")
    print("-" * 30)
    print(df.head())

if __name__ == "__main__":
    download_fed_rate()
    