import pandas as pd
from io import StringIO

from settings import ALPHA_VANTAGE_API_KEY, RAPIDAPI_API_KEY
import alphavantage as av
import yahoofinance as yf
import worldbank as wb

ticker = "^DJI"

csv = yf.get_historical_data_v7(symbol=ticker)

df = pd.read_csv(StringIO(csv))
df['Date'] = pd.to_datetime(df['Date'])
df.set_index("Date", inplace=True)
df.to_pickle(f"{ticker}_prices.pickle")

# csv = wb.real_gdp_world()
# print(csv)
