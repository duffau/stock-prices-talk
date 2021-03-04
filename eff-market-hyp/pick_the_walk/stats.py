import scipy.stats as sps
import matplotlib.pyplot as plt
import numpy as np

PLOT_COL = "#7e1e9c"

def calc_stats(correct_counts, wrong_counts):
    assert len(correct_counts) ==  len(wrong_counts), "correct_counts and wrong_counts must have equal length"
    n_trials = sum(correct_counts) + sum(wrong_counts)
    n_correct = sum(correct_counts)
    n_wrong = sum(wrong_counts)
    null_hypothesis_success_rate = 0.5
    try:
        mean_success_rate = n_correct/n_trials
        std_error = (mean_success_rate*(1-mean_success_rate)/n_trials)**0.5
        t_value = (mean_success_rate - null_hypothesis_success_rate)/std_error
        df = n_trials - 1
        p_value = (1-sps.t.cdf(abs(t_value), df))*2
    except ZeroDivisionError:
        mean_success_rate, std_error, p_value, df = None, None, None, None

    return null_hypothesis_success_rate, mean_success_rate, std_error, p_value, df 


def plot_stats(ax, null_hypothesis_success_rate, mean_success_rate, std_error, p_value, df):
    if mean_success_rate is not None:
        x = np.linspace(0, 1, num=100)
        y = sps.t.pdf(x, loc=null_hypothesis_success_rate, scale=std_error, df=df)
        y_max = max(y)
        ax.plot(x, y, 'black', lw=2)
        left_conf = null_hypothesis_success_rate - abs(null_hypothesis_success_rate - mean_success_rate)
        right_conf = null_hypothesis_success_rate + abs(null_hypothesis_success_rate - mean_success_rate)
        ax.fill_between(x, y, where=x<left_conf, alpha=0.5, color=PLOT_COL)
        ax.fill_between(x, y, where=x>right_conf, alpha=0.5, color=PLOT_COL)
        is_left = (null_hypothesis_success_rate - mean_success_rate) > 0 
        ax.axvline(x=mean_success_rate, color="black", lw=3)
        ax.annotate(f"mean success rate: {mean_success_rate*100:.0f}%",
                xy=(mean_success_rate, y_max*0.5), xycoords='data',
                xytext=(
                    0.0 if is_left else 0.6, 
                    y_max*0.6
                ), 
                textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc3,rad=-0.3"),
                )
        tail_prob = p_value/2
        ax.annotate(f"{tail_prob*100:.0f}%",
                xy=(left_conf-0.05, y_max*0.05), xycoords='data',
                xytext=(0.1, y_max*0.33), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc3,rad=-0.3"),
                )
        ax.annotate(f"{tail_prob*100:.0f}%",
                xy=(right_conf+0.05, y_max*0.05), xycoords='data',
                xytext=(0.9, y_max*0.33), textcoords='data',
                arrowprops=dict(arrowstyle="->",
                                connectionstyle="arc3,rad=0.3"),
                )
    else:
        ax.text(0.5, 0.5, "Nothing to plot",  ha='center', va='center')
    return ax

if __name__ == "__main__":
    import numpy.random as nprand

    correct_counts = nprand.randint(0,5, size=10)
    wrong_counts = 5 - correct_counts
    null_hypothesis_success_rate = 0.5
    mean_success_rate, std_error, p_value, df = calc_stats(correct_counts, wrong_counts)
    plt.xkcd()
    fig, ax = plt.subplots()
    fig.set_size_inches(6.4, 3.0)
    plot_stats(ax, null_hypothesis_success_rate, mean_success_rate, std_error, p_value, df)
    plt.savefig('norm.png')
