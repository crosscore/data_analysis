import scipy.stats as stats

# Calculate the 95% chi-square value for degrees of freedom from 1 to 10
df_range = range(1, 11)
chi2_values = [stats.chi2.ppf(0.025, df) for df in df_range]

# show results
for df, value in zip(df_range, chi2_values):
    print(f"Degree of freedom {df}: Chi-square value with 2.5% confidence interval = {value:.4f}")