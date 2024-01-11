import numpy as np
from scipy import stats

# Generate random sample data from normal distribution (15 pieces)
np.random.seed(42)
sample_data = np.random.normal(loc=0, scale=1, size=15)

# excute shapiro-wilk test
W_statistic, p_value = stats.shapiro(sample_data)

W_statistic, p_value
