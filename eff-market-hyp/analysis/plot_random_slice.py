import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy.random 

def random_walk(mean, std, n):
    eps = numpy.random.normal(0.0, scale=std, size=n)
    y = numpy.empty(shape=(n,))
    y[0] = eps[0]
    for i in range(1, len(eps)):
        y[i] = y[i-1] + eps[i]
    return y + mean

ticker = "^DJI"
var = "Adj Close"
interval_length = 100
mean = 4000
std = 1
df_prices = pd.read_pickle(f"{ticker}_prices.pickle")
mean = df_prices[var].diff().mean()
std = df_prices[var].diff().std()
print(f"mean = {mean}")
print(f"std = {std}")
df_prices["random_walk"] = random_walk(mean=mean, std=std, n=len(df_prices))
start = random.randint(0, len(df_prices) - interval_length)
end = start + interval_length

df_prices.iloc[start:end,:].plot(y=var)
plt.savefig(f"plots/{ticker}_{var}.png")
plt.close()

df_prices.iloc[start:end,:].plot(y="random_walk")
plt.savefig(f"plots/random_walk.png")
plt.close()
