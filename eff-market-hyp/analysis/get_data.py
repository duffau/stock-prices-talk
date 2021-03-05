import pandas as pd
from io import StringIO

from settings import ALPHA_VANTAGE_API_KEY, RAPIDAPI_API_KEY
from apis import alphavantage as av
from apis import yahoofinance as yf
from apis import worldbank as wb

tickers = ["^GSPC", "TSLA", "^DJI", "GME", "HPE", "GOOG"]
data_dir = "./data"
for ticker in tickers:
    print(f"Getting {ticker}...")
    csv = yf.get_historical_data_v7(symbol=ticker)
    df = pd.read_csv(StringIO(csv))
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index("Date", inplace=True)
    df.to_pickle(f"{data_dir}/{ticker}_prices.pickle")
