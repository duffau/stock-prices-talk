from pathlib import Path 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

var = "Adj Close"
dataset_paths = Path("./data").glob("*_prices.pickle")
use_cols_ticker = ["Ticker","Name", "Exchange"]
ticker_paths = Path("./data/").glob("yahoo-ticker-symbols-*.csv")
tickers = pd.concat(
    [pd.read_csv(ticker_path, usecols=use_cols_ticker) for ticker_path in ticker_paths], 
    ignore_index=True
)

fig_ret, axs_ret = plt.subplots(2, 3, figsize=(9, 5.8), tight_layout=True)
fig_acf, axs_acf = plt.subplots(2, 3, figsize=(9, 5.8), tight_layout=True)
fig_acf_sq, axs_acf_sq = plt.subplots(2, 3, figsize=(9, 5.8), tight_layout=True)

for ax_ret, ax_acf, ax_acf_sq, dataset_path in zip(axs_ret.reshape(-1), axs_acf.reshape(-1), axs_acf_sq.reshape(-1), dataset_paths):
    print(dataset_path)
    ticker_symb, *ignore = dataset_path.stem.split("_")
    try:
        ticker_info = tickers[tickers.Ticker == ticker_symb]
        ticker_name = ticker_info.Name.values[0]
    except Exception:
        ticker_name = ticker_symb
    df_prices = pd.read_pickle(dataset_path)
    y = np.log(df_prices[var]).diff()
    y = y[~np.isnan(y)]

    ax_ret.plot(y)
    ax_ret.set_title(ticker_name)
    
    sm.graphics.tsa.plot_acf(y, ax=ax_acf, lags=40)
    ax_acf.set_title(ticker_name)

    sm.graphics.tsa.plot_acf(y**2, ax=ax_acf_sq, lags=40)
    ax_acf.set_title(ticker_name)


fig_ret.savefig(f"plots/returns.svg")
plt.close(fig_ret)

fig_acf.savefig(f"plots/acf_returns.svg")
plt.close(fig_acf)

fig_acf_sq.savefig(f"plots/acf_returns_sq.svg")
plt.close(fig_acf_sq)
