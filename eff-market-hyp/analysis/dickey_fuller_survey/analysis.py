import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path 
import statsmodels.tsa.stattools as st
import seaborn as sns

var = "Adj Close"
dataset_paths = Path("./data").glob("*_prices.pickle")
adf_results = []

for dataset_path in dataset_paths:
    print(dataset_path)
    ticker, security, *ignore =  dataset_path.name.split("_")
    print(ticker, security)
    df_prices = pd.read_pickle(dataset_path)
    df_prices.dropna(inplace=True)
    try:
        res = st.adfuller(df_prices[var], regression="ct")
        adf_result = {"security": security, "ticker": ticker, "adf_p_value": res[1]}
        adf_results.append(adf_result)
    except ValueError as e:
        print(f"Can't run ADF test on security: {security}, ticker: {ticker}: {repr(e)}")
adf_results = pd.DataFrame.from_records(adf_results)
adf_results.to_pickle("./tables/adf_results.pickle")
