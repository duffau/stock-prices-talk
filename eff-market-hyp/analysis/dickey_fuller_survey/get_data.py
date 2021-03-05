import pandas as pd
from io import StringIO
from pathlib import Path

from apis import yahoofinance as yf
from apis  import worldbank as wb

SECURITIES = ["stocks", "etf", "index", "mutual-fund", "currency"]
SEED = 123
N_DOWNLOADS = 10
OBS_LOWER_LIMIT = 100
all_downloaded_datasets = Path("./data").glob("*")


for security in SECURITIES:
    n_found = 0
    tickers = pd.read_csv(f"../data/yahoo-ticker-symbols-{security}.csv", usecols=["Ticker"])
    print(f"Sampling from {len(tickers)} {security} tickers")
    while n_found < N_DOWNLOADS: 
        ticker = tickers.sample(n=1, random_state=SEED).Ticker.values[0]
        SEED += 1
        file_path = f"./data/{ticker}_{security}_prices.pickle"
        print(f"Trying ticker: {security} {ticker} ...")
        if file_path in all_downloaded_datasets:
            print("Found in folder. Skipping ...")
            continue
        csv = yf.get_historical_data_v7(symbol=ticker)
        df = pd.read_csv(StringIO(csv))
        print(f"Downloaded {len(df)} rows for ticker: {security} {ticker}")
        if len(df) > OBS_LOWER_LIMIT:
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index("Date", inplace=True)
            df.to_pickle(file_path)
            n_found += 1

    print(f"Downloaded {security} {n_found} datasets")
