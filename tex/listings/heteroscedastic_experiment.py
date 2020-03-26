import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression

thetas = np.array([2, 5, 1])
def f(X):
    return np.dot(X, thetas)

d1, d2, d3 = 6, 4 , 2

def d_lower(x1, x2, d1, d2, d3):
    return 1/4 * (d1 + d3 + 2*d1*x2 - 2*d3*x2 - 2*d2*x2 + (d1 + d2)*x1**2 + (d2 + d2)*x2**2)

points = np.array([
    [1, 1],
    [-1, 1],
    [-1, -1]
])

n_trials = 5
results = []

np.random.seed(42)

def make_y(X):
    N = X.shape[0]
    error_dispersions = d_lower(X[:, 1], X[:, 2], d1, d2, d3)
    errors = np.random.normal(0, np.sqrt(error_dispersions), N)
    return f(X) + errors 

Ns = np.arange(1, 10) * 3
for _ in range(n_trials):
    for N in Ns:
        result = {
            'N': N
        }
        Xs = [
            ('optimal', np.repeat(points, N / 3, axis=0)),
            ('random', np.random.uniform(-1, 1, (N, 2)))
        ]
        for name, X in Xs:
            X = np.concatenate([np.ones((N, 1)), X], axis=1)
            y = make_y(X)
            error_dispersions = d_lower(X[:, 1], X[:, 2], d1, d2, d3)
            weights = 1 / error_dispersions
            wls_estimator = LinearRegression(fit_intercept=False).fit(X, y, weights)
            result[f'theta_{name}_mse'] = mean_squared_error(thetas, wls_estimator.coef_)
        results.append(result)
    
df = pd.DataFrame(results)

df_agg = df.groupby('N').agg(['mean', 'std'])
df_agg.columns = [f'{agg_name}_{column}' for (column, agg_name) in df_agg.columns]

ax = plt.gca()
for name in ['optimal', 'random']:
    mean = df_agg[f'mean_theta_{name}_mse'].values
    ax.plot(Ns, mean, '.-', label=f'mean_theta_{name}_mse') 
    mean = df_agg[f'mean_theta_{name}_mse']
    std = df_agg[f'std_theta_{name}_mse']
    ax.fill_between(Ns, mean - std, mean + std, alpha=0.2)
ax.legend()
ax.set_title('Optimal design vs random MSE')
ax.set_xticks(Ns)
ax.set_xticklabels(Ns)
ax.set_xlabel('N observations')
ax.set_ylabel('MSE')

plt.gcf().savefig('tex/images/heteroscedastic-experiment.png')
