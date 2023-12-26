import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import os

def is_normal(data, test_type="shapiro"):
    """Check for normality using either Shapiro-Wilk or Kolmogorov-Smirnov test"""
    if len(data) < 3:
        print("Not enough data to perform normality test")
        return False
    if test_type == "shapiro":
        print("Check for normality using Shapiro-Wilk test")
        stat, p = stats.shapiro(data)
    elif test_type == "ks":
        print("Check for normality using Kolmogorov-Smirnov")
        stat, p = stats.kstest(data, 'norm')
    return p > 0.05

def check_equal_variance(df1, df2, column):
    """Check for equal variance using Levene's test"""
    stat, p = stats.levene(df1[column], df2[column])
    return p > 0.05

def compare_groups(df1, df2, column):
    # Check if data is empty or too small
    if df1[column].empty or df2[column].empty or len(df1[column]) < 3 or len(df2[column]) < 3:
        print(f"Insufficient data in one of the groups for column '{column}'. Skipping test.")
        return None
    # Determine which normality test to use based on sample size
    normal_test_type = "shapiro" if len(df1[column]) < 5000 else "ks"
    # Normality check
    if is_normal(df1[column], normal_test_type) and is_normal(df2[column], normal_test_type):
        # Checking for equal variance
        if check_equal_variance(df1, df2, column):
            print("Equal variance: Use standard t-test")
            stat, p = stats.ttest_ind(df1[column], df2[column])
        else:
            print("Unequal variance: Use Welch's t-test")
            stat, p = stats.ttest_ind(df1[column], df2[column], equal_var=False)
    else:
        print("Use Mann-Whitney U test for non-normal distributions")
        stat, p = stats.mannwhitneyu(df1[column], df2[column])
    return p


df = pd.read_csv('../data/csv/outlier_removed/device_outlier_removed.csv', dtype={'user': str})

df_1st_half = df[df['days'] == '1st_half']
df_2nd_half = df[df['days'] == '2nd_half']

print(df_1st_half['category'].value_counts(dropna=False))
print(df_2nd_half['category'].value_counts(dropna=False))

results = {}
significance_level = 0.05
for category in df['category'].unique():
    print(category)
    df1 = df_1st_half[df_1st_half['category'] == category]
    df2 = df_2nd_half[df_2nd_half['category'] == category]
    p_value = compare_groups(df1, df2, 'duration')
    if p_value is not None:
        result = "/   /Significant difference/   /" if p_value < significance_level else "No significant difference"
    else:
        result = "Insufficient data to determine significance..."
    results[category] = (result, p_value)
print('------------')
for category, (result, p_value) in results.items():
    print(f"{category}: {result}, p-value = {p_value:.33f}")
print('------------')

total_duration_exp1 = df_1st_half.groupby('category')['duration'].sum().reset_index()
total_duration_exp2 = df_2nd_half.groupby('category')['duration'].sum().reset_index()

total_duration_exp1['Experiment'] = 'Exp1'
total_duration_exp2['Experiment'] = 'Exp2'
total_duration = pd.concat([total_duration_exp1, total_duration_exp2])

# Create a list of categories judged to be significant differences
significant_categories = [category for category, (result, _) in results.items() if "Significant difference" in result]

plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")
palette = sns.color_palette("hls", len(total_duration['category'].unique()))
bar_plot = sns.barplot(x="category", y="duration", hue="Experiment", data=total_duration, palette=palette)

plt.title('Total Duration by category for Each Experiment Period')
plt.xlabel('category')
plt.ylabel('Total Duration')
plt.xticks(rotation=270)
plt.legend(title='Experiment')
plt.subplots_adjust(bottom=0.3)

for label in bar_plot.get_xticklabels():
    if label.get_text() in significant_categories:
        label.set_color('crimson')

output_file = '../../data/img/TV_duration_2exp/total_duration_by_category.png'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
plt.savefig(output_file)