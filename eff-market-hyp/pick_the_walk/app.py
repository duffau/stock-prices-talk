from io import BytesIO
import random

import numpy as np
import pandas as pd

from flask import Flask, send_file, render_template, request, redirect, url_for

# import matplotlib
# matplotlib.use('agg')
import matplotlib.pyplot as plt


# styling

import os, sys
import plot_random_slice as prs
import stats as sts

app = Flask(__name__)

plt.xkcd()
RANDOM_WALK_PLOT_URL = "/randomwalk.png"
STOCK_PRICE_PLOT_URL = "/stockprice.png"
CORRECT_COUNTS = []
WRONG_COUNTS = []

ticker = "^DJI"
VAR = "Adj Close"
INTERVAL_LENGTH = 100
DF_PRICES = pd.read_pickle(f"{ticker}_prices.pickle")
try:
    NO_CLUES = not bool(sys.argv[1])
except IndexError:
    NO_CLUES = True

try:
    PORT = int(sys.argv[2])
except IndexError:
    PORT = 5000

# Pre-calculate a random walk series.
mean = DF_PRICES[VAR].diff().mean()
std = DF_PRICES[VAR].diff().std()
DF_PRICES["random_walk"] = prs.random_walk(mean=mean, std=std, n=len(DF_PRICES))


@app.route('/', methods=["GET"])
def frontpage():
    plot_urls = [RANDOM_WALK_PLOT_URL, STOCK_PRICE_PLOT_URL]
    random.shuffle(plot_urls)
    left_plot, right_plot = plot_urls
    print(f"LEFT: {left_plot}, RIGHT: {right_plot}")
    return render_template('index.html', left_plot=left_plot, right_plot=right_plot)

@app.route('/', methods=["POST"])
def register_counts():
    score_left = to_int(request.form['score_left'])
    score_right = to_int(request.form['score_right'])

    CORRECT_COUNTS.append(score_left)
    WRONG_COUNTS.append(score_right)
    print(CORRECT_COUNTS)
    print(WRONG_COUNTS)
    return redirect(url_for('frontpage'))

@app.route('/clear', methods=["GET"])
def clear_counts():
    global CORRECT_COUNTS
    global WRONG_COUNTS 
    CORRECT_COUNTS = []
    WRONG_COUNTS = []
    return redirect(url_for('frontpage'))


def to_int(s):
    try:
        return int(s)
    except ValueError:
        return 0

@app.route('/randomwalk.png')
def plot_randomwalk():
    fig, ax = plt.subplots()
    color = "b"
    var = "random_walk"
    interval_length = INTERVAL_LENGTH
    prs.draw_random_time_slice(ax, DF_PRICES, var, interval_length, color, NO_CLUES)
    return nocache(fig_response(fig))

@app.route('/stockprice.png')
def plot_stockprice():
    fig, ax = plt.subplots()
    color = "r"
    var = VAR
    interval_length = INTERVAL_LENGTH
    prs.draw_random_time_slice(ax, DF_PRICES, var, interval_length, color, NO_CLUES)
    return nocache(fig_response(fig))

@app.route('/norm.png')
def plot_stats():
    fig, ax = plt.subplots()
    fig.set_size_inches(6.4, 3.0)
    null_hypothesis_success_rate, mean_success_rate, std_error, p_value, df = sts.calc_stats(CORRECT_COUNTS, WRONG_COUNTS) 
    sts.plot_stats(ax, null_hypothesis_success_rate, mean_success_rate, std_error, p_value, df)
    return nocache(fig_response(fig))


@app.route("/stats")
def stats():
    return render_template("stats.html", plot="/norm.png")

def draw_random_scatter(ax, color):
    """Draw a random scatterplot"""
    x = [random.random() for i in range(100)]
    y = [random.random() for i in range(100)]
    ax.scatter(x, y, color=color)

def fig_response(fig):
    """Turn a matplotlib Figure into Flask response"""
    img_bytes = BytesIO()
    if NO_CLUES:
        fig.tight_layout()
    fig.savefig(img_bytes)
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png')

def nocache(response):
    """Add Cache-Control headers to disable caching a response"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    return response

app.run(port=PORT)
