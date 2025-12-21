import pandas as pd
from itertools import combinations

def get_ticker_pairs(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Check if 'Sector' and 'Symbol' columns exist
    if 'Sector' not in df.columns or 'Symbol' not in df.columns:
        raise ValueError("The CSV must contain 'Sector' and 'Symbol' columns.")
    
    # Filter out 'Unknown' sectors
    df = df[df['Sector'] != 'Unknown']
    df = df.dropna(subset=['Sector'])

    # 1. Divide tickers by departments (Sector) and count elements
    sector_counts = df['Sector'].value_counts()
    
    # 2. Take the top 5 departments with the most elements
    top_5_sectors = sector_counts.head(5).index.tolist()
    print(f"Top 5 Sectors: {top_5_sectors}")
    
    # Filter data for these sectors
    df_top = df[df['Sector'].isin(top_5_sectors)]
    
    results = []
    
    # 3. Create a mapping of tickerA, tickerB, sector for every pair
    for sector in top_5_sectors:
        tickers = df_top[df_top['Sector'] == sector]['Symbol'].tolist()
        # Generate pairs (order doesn't matter for pairs, using combinations)
        # If order matters (A,B is diff from B,A), use permutations. 
        # Usually "pairs" implies combinations.
        pairs = list(combinations(tickers, 2))
        
        for t1, t2 in pairs:
            results.append({
                'tickerA': t1,
                'tickerB': t2,
                'sector': sector
            })
            
    return pd.DataFrame(results)

if __name__ == "__main__":
    file_path = r"/home/alexis/Documents/EPFL/ADA/ada-2025-project-t4d4/data/symbols_valid_meta_augmented_with_dates.csv"
    try:
        pairs_df = get_ticker_pairs(file_path)
        print(f"Generated {len(pairs_df)} pairs.")
        print("First 5 pairs:")
        print(pairs_df.head())
        
        # Optional: Save to file if needed
        pairs_df.to_csv("ticker_sector_pairs.csv", index=False)
        
    except Exception as e:
        print(f"Error: {e}")
