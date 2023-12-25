import pandas as pd
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import os

df = pd.read_csv('../../data/csv/outlier_removed/MBapp_MBweb_PC_TV_outlier_removed.csv', dtype={'user': str})

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

for source_name in df['source_name'].unique():
    df1 = df_exp1[df_exp1['source_name'] == source_name]
    df2 = df_exp2[df_exp2['source_name'] == source_name]
    p_value = compare_groups(df1, df2, 'duration')
    result = "Significant difference" if p_value < significance_level else "No significant difference"
    results[source_name] = (result, p_value)

for source_name, (result, p_value) in results.items():
    print(f"{source_name}: {result}, p-value = {p_value:.33f}")


df_exp1 = df_exp1[(df_exp1['source_name'] == 'MobileApp') | (df_exp1['source_name'] == 'MobileWeb')]
df_exp2 = df_exp2[(df_exp2['source_name'] == 'MobileApp') | (df_exp2['source_name'] == 'MobileWeb')]
total_duration_exp1 = df_exp1.groupby('source_name')['duration'].sum().reset_index()
total_duration_exp2 = df_exp2.groupby('source_name')['duration'].sum().reset_index()

total_duration_exp1['Experiment'] = 'Exp1'
total_duration_exp2['Experiment'] = 'Exp2'
total_duration = pd.concat([total_duration_exp1, total_duration_exp2])

sns.set(style="whitegrid")
palette = sns.color_palette("hls", len(total_duration['source_name'].unique()))
sns.barplot(x="source_name", y="duration", hue="Experiment", data=total_duration, palette=palette)

plt.title('Total Duration by Source Name for Each Experiment Period')
plt.xlabel('Source Name')
plt.ylabel('Total Duration')
plt.legend(title='Experiment')
output_file = '../../data/img/MB_PC_TV_duration_2exp/total_duration_by_source_name_2.png'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
plt.savefig(output_file, dpi=300)