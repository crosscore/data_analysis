import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns

n_iterations = 1000
p_values = []

for _ in range(n_iterations):
    sample_data = np.random.normal(loc=20, scale=1, size=15)
    _, p_value = stats.shapiro(sample_data)
    p_values.append(p_value)

print(p_values)
error_rate = sum(p_val < 0.05 for p_val in p_values) / n_iterations

sns.set_style('whitegrid')
plt.figure(figsize=(10, 6))

bins_sturges = int(np.ceil(np.log2(n_iterations) + 1))
print(bins_sturges)
sns.histplot(p_values, bins=bins_sturges, color='crimson', edgecolor='black', alpha=0.7)
plt.xlabel('p-value')
plt.ylabel('Frequency')
plt.title('Distribution of p-values for Shapiro-Wilk test')
plt.savefig('../data/img/shapiro-wilk_test.png')
print(error_rate)
plt.close('all')