import numpy as np
import scipy.stats as sts
import matplotlib.pyplot as plt

def random_walk(drift=0, std=.1, n=100, alpha=0.95):
    eps = np.random.normal(0.0, scale=std, size=n)
    y = np.empty(shape=(n,))
    y_mean = np.empty(shape=(n,))
    y_lower = np.empty(shape=(n,))
    y_upper = np.empty(shape=(n,))
    y[0] = eps[0]
    y_mean[0] = 0.0
    x = abs(sts.norm.ppf((1-alpha)/2))
    for i in range(1, len(eps)):
        y[i] = drift + y[i-1] + eps[i]
        y_mean[i] = drift + y_mean[i-1]
        y_lower[i] = y_mean[i] - std*x*(i**0.5)
        y_upper[i] = y_mean[i] + std*x*(i**0.5)
    return y, y_mean, y_lower, y_upper


n = 1000

drift = 0.0
rw, rw_mean, rw_lower, rw_upper = random_walk(n=n, drift=drift)
plt.plot(rw)
plt.plot(rw_mean, 'k--')
plt.plot(rw_lower, 'k')
plt.plot(rw_upper, 'k')
plt.title(f"Random walk - n={n}, drift={drift}")
plt.savefig("./plots/rw.svg")
plt.close()

drift = 0.01
rw, rw_mean, rw_lower, rw_upper = random_walk(n=n, drift=drift)
plt.plot(rw)
plt.plot(rw_mean, 'k--')
plt.plot(rw_lower, 'k')
plt.plot(rw_upper, 'k')
plt.title(f"Random walk - n={n}, drift={drift}")
plt.savefig("./plots/rw1.svg")
plt.close()
