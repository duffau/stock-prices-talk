import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path 

time_intervals = {
    "full": (0,-1),
    "1year": (-253,-1)
}

var = "Adj Close"
dataset_paths = Path("./data").glob("*_prices.pickle")
use_cols_ticker = ["Ticker","Name", "Exchange"]
ticker_paths = Path("./data/").glob("yahoo-ticker-symbols-*.csv")
tickers = pd.concat(
    [pd.read_csv(ticker_path, usecols=use_cols_ticker) for ticker_path in ticker_paths], 
    ignore_index=True
)
for dataset_path in dataset_paths:
    print(dataset_path)
    ticker_symb, *ignore = dataset_path.stem.split("_")
    try:
        ticker_info = tickers[tickers.Ticker == ticker_symb]
        ticker_name = ticker_info.Name.values[0]
    except Exception:
        ticker_name = ticker_symb
    for ti_name, ti in time_intervals.items():
        start, end = ti
        df_prices = pd.read_pickle(dataset_path)
        df_prices.iloc[start:end,:].plot(y=var)
        plt.title(ticker_name)
        plt.savefig(f"plots/{dataset_path.stem}_{ti_name}.svg")
        plt.close()
