import pandas as pd
import matplotlib.pyplot as plt

ticker = "^DJI"
var = "Adj Close"
df_prices = pd.read_pickle(f"{ticker}_prices.pickle")

df_prices.plot(y=var)
plt.savefig(f"plots/{ticker}_{var}.png")
plt.close()
