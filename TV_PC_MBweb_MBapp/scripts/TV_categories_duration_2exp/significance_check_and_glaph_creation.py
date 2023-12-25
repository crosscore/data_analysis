import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import os

df = pd.read_csv('../../data/csv/outlier_removed/TV_outlier_removed.csv', dtype={'user': str})

start_date_exp1 = '2022-10-22'
end_date_exp1 = '2022-11-04'
df_exp1 = df[(df['date'] >= start_date_exp1) & (df['date'] <= end_date_exp1)]
df_exp2 = df[(df['date'] < start_date_exp1) | (df['date'] > end_date_exp1)]

def is_normal(data, test_type="shapiro"):
    """Check for normality using either Shapiro-Wilk or Kolmogorov-Smirnov test"""
    if test_type == "shapiro":
        print("Check for normality using Shapiro-Wilk test test")
        stat, p = stats.shapiro(data)
    elif test_type == "ks":
        print("Check for normality using Kolmogorov-Smirnov test")
        stat, p = stats.kstest(data, 'norm')
    return p > 0.05

def compare_groups(df1, df2, column):
    # Determine which normality test to use based on sample size
    normal_test_type = "shapiro" if len(df1[column]) < 5000 else "ks"
    if is_normal(df1[column], normal_test_type) and is_normal(df2[column], normal_test_type):
        # Use t-test for normal distributions
        stat, p = stats.ttest_ind(df1[column], df2[column])
    else:
        # Use Mann-Whitney U test for non-normal distributions
        stat, p = stats.mannwhitneyu(df1[column], df2[column])
    return p

results = {}
significance_level = 0.05

for tv_category in df['tv_category'].unique():
    print(tv_category)
    df1 = df_exp1[df_exp1['tv_category'] == tv_category]
    df2 = df_exp2[df_exp2['tv_category'] == tv_category]
    p_value = compare_groups(df1, df2, 'duration')
    result = "Significant difference" if p_value < significance_level else "No significant difference"
    results[tv_category] = (result, p_value)

for tv_category, (result, p_value) in results.items():
    print(f"{tv_category}: {result}, p-value = {p_value:.33f}")


# df_exp1 = df_exp1[(df_exp1['tv_category'] == 'MobileApp') | (df_exp1['tv_category'] == 'MobileWeb')]
# df_exp2 = df_exp2[(df_exp2['tv_category'] == 'MobileApp') | (df_exp2['tv_category'] == 'MobileWeb')]
total_duration_exp1 = df_exp1.groupby('tv_category')['duration'].sum().reset_index()
total_duration_exp2 = df_exp2.groupby('tv_category')['duration'].sum().reset_index()

total_duration_exp1['Experiment'] = 'Exp1'
total_duration_exp2['Experiment'] = 'Exp2'
total_duration = pd.concat([total_duration_exp1, total_duration_exp2])

sns.set(style="whitegrid")
palette = sns.color_palette("hls", len(total_duration['tv_category'].unique()))
sns.barplot(x="tv_category", y="duration", hue="Experiment", data=total_duration, palette=palette)

plt.title('Total Duration by Source Name for Each Experiment Period')
plt.xlabel('Source Name')
plt.ylabel('Total Duration')
plt.legend(title='Experiment')
output_file = '../../data/img/TV_duration_2exp/total_duration_by_tv_category.png'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
plt.savefig(output_file, dpi=300)