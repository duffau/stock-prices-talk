import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy.random 

    

def draw_random_time_slice(ax, df_prices, var, interval_length, color, no_clues=True):
    start = random.randint(0, len(df_prices) - interval_length)
    end = start + interval_length
    df_prices.iloc[start:end,:].plot(
        y=var, ax=ax, 
        color=color if not no_clues else 'black', 
        legend=not no_clues
    )
    if no_clues:
        x_axis = ax.axes.get_xaxis()
        x_axis.set_visible(False)
        y_axis = ax.axes.get_yaxis()
        y_axis.set_visible(False)
    return ax

def random_walk(mean, std, n):
    eps = numpy.random.normal(0.0, scale=std, size=n)
    y = numpy.empty(shape=(n,))
    y[0] = eps[0]
    for i in range(1, len(eps)):
        y[i] = y[i-1] + eps[i]
    return y + mean
