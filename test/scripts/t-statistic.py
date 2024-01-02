import numpy as np
import scipy.stats as stats

# Randomly generate data for two groups
np.random.seed(42) # Set random number seed
group_A = np.random.normal(170, 10, 50) # mean 70, standard deviation 10, number of data 30
group_B = np.random.normal(165, 10, 50) # mean 75, standard deviation 10, number of data 30
print(group_A)
print(group_B)

# Perform a two-group independent t-test
t_stat, p_value = stats.ttest_ind(group_A, group_B)

print("t-statistic:", t_stat)
print("p-value:", p_value)
