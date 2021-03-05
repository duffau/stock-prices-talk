import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path 


var = "Adj Close"
dataset_paths = Path("./data").glob("*_prices.pickle")

for dataset_path in dataset_paths:
    print(dataset_path)
    df_prices = pd.read_pickle(dataset_path)
    df_prices.plot(y=var)
    plt.savefig(f"plots/{dataset_path.stem}.png")
    plt.close()
