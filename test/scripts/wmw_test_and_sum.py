import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

np.random.seed(0)

group_A = np.random.normal(50, 5, 100)
print(group_A, group_A.sum())
# Adjust group B to have a similar sum to group A but a different distribution
group_B = np.random.uniform(45, 55, 100)  # Adjusted to have a similar sum to group A
print(group_B, group_B.sum())
# Adjust the scale of the exponential distribution for group C
group_C = np.random.exponential(scale=1/0.05, size=100) + 30.5  # Adjusted scale and shift to match sum of group A
print(group_C, group_C.sum())

# Mann-Whitney U test between group A and group B
u_stat_AB, p_value_AB = stats.mannwhitneyu(group_A, group_B)
# Mann-Whitney U test for group A and group C
u_stat_AC, p_value_AC = stats.mannwhitneyu(group_A, group_C)

# Check if p-value is less than 5%
significant_AB = p_value_AB < 0.05
significant_AC = p_value_AC < 0.05


# Create plot for histograms
plt.figure(figsize=(15, 10))

# Histogram of groups A and B
plt.subplot(2, 2, 1)
plt.hist(group_A, bins=20, alpha=0.7, label='Group A')
plt.hist(group_B, bins=20, alpha=0.7, label='Group B')
plt.title(f'Histogram of Group A vs Group B\np-value: {p_value_AB:.4f} - {"Significant" if significant_AB else "Not Significant"}')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()

# Histogram of groups A and C
plt.subplot(2, 2, 2)
plt.hist(group_A, bins=20, alpha=0.7, label='Group A')
plt.hist(group_C, bins=20, alpha=0.7, label='Group C')
plt.title(f'Histogram of Group A vs Group C\np-value: {p_value_AC:.4f} - {"Significant" if significant_AC else "Not Significant"}')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()

# Sum of each group
sum_A, sum_B, sum_C = np.sum(group_A), np.sum(group_B), np.sum(group_C)

# Bar plot for sums
plt.subplot(2, 1, 2)
plt.bar(['Group A', 'Group B', 'Group C'], [sum_A, sum_B, sum_C])
plt.title('Sum of Values in Each Group')
plt.ylabel('Sum of Values')

# Show plot
plt.tight_layout()
plt.savefig('../data/img/wmw_test_and_sum.png')

# Print the p-value and sum results
p_value_AB, p_value_AC, significant_AB, significant_AC, sum_A, sum_B, sum_C

