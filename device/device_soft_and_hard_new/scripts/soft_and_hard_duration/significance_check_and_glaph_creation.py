#significance_check_and_glaph_creation.py
import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import os

def is_normal(data, test_type="shapiro"):
    """
    Assess the normality of a dataset. The Shapiro-Wilk test is used for small samples (< 5000 data points),
    which is more appropriate for detecting deviations from normality. For larger samples, the 
    Kolmogorov-Smirnov test is used as it's less sensitive to slight deviations from a normal distribution.
    
    Parameters:
        data (array_like): The data to be tested for normality.
        test_type (str): The type of normality test to perform ('shapiro' or 'ks').
        
    Returns:
        bool: True if the data is normally distributed, False otherwise.
    """
    if len(data) < 3:
        print("Not enough data to perform a normality test.")
        return False
    if test_type == "shapiro":
        print("Performing the Shapiro-Wilk test to check for normality. (< 5000 data points)")
        stat, p = stats.shapiro(data)
    elif test_type == "ks":
        print("Performing the Kolmogorov-Smirnov test to check for normality in a larger sample.")
        stat, p = stats.kstest(data, 'norm')
    # A p-value greater than the threshold (0.05) suggests normal distribution
    is_normal = p > 0.05
    if is_normal:
        print(f"The data follows a normal distribution (p-value: {p:.33f}).")
    else:
        print(f"The data does not follow a normal distribution (p-value: {p:.33f}).")
    return is_normal

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
    significance = "Significant" if p < 0.05 else "Not significant"
    print(f"========================\np-value: {p:.18f} - {significance}\n========================\n")
    return p, significance

def plot_boxplot(df, category_col, period_col, duration_col, output_file, category_results):
    plt.figure(figsize=(12, 8))
    ax = sns.boxplot(x=category_col, y=duration_col, hue=period_col, data=df, palette="hls")
    plt.title('Boxplot of Duration by Category and Experiment Period')
    for cat, p_val, signif in category_results:
        plt.text(df[category_col].unique().tolist().index(cat), df[duration_col].max(), f'p={p_val:.4f}, {signif}', ha='center', color='crimson', alpha=0.7)    
    plt.xlabel(category_col)
    plt.ylabel('Duration')
    plt.xticks(rotation=0)
    plt.legend(title=period_col)
    plt.savefig(output_file)

def plot_scatter(df, category_col, period_col, duration_col, output_file, category_results):
    plt.figure(figsize=(12, 8))
    categories = df[category_col].unique()
    periods = df[period_col].unique()
    palette = sns.color_palette("hls", len(periods))
    category_indices = {category: index for index, category in enumerate(categories)}
    offset = np.linspace(-0.2, 0.2, len(periods))
    # Settings to add jitter
    jitter_amount = 0.15
    for category in categories:
        for period, color, off in zip(periods, palette, offset):
            period_index = category_indices[category] + off
            period_df = df[(df[category_col] == category) & (df[period_col] == period)]
            if not period_df.empty:
                # Add jitter and adjust alpha value and data point size
                jittered_x = np.random.uniform(-jitter_amount, jitter_amount, size=period_df.shape[0]) + period_index
                plt.scatter(jittered_x, period_df[duration_col], color=color, alpha=0.5, s=10, label=f'{category} ({period})')
    for cat, p_val, signif in category_results:
        plt.text(category_indices[cat], df[duration_col].max(), f'p={p_val:.4f}, {signif}', ha='center', color='crimson', alpha=0.7)
    plt.title('Scatter Plot of Duration for Each Category by Period')
    plt.xlabel(category_col)
    plt.ylabel(duration_col)
    plt.legend(title=period_col, loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.xticks(ticks=np.arange(len(categories)), labels=categories)
    plt.subplots_adjust(right=0.8)
    plt.savefig(output_file)


def plot_violin(df, category_col, period_col, duration_col, output_file, category_results):
    plt.figure(figsize=(12, 8))
    ax = sns.violinplot(x=category_col, y=duration_col, hue=period_col, data=df, palette="hls", split=True)
    for patch in ax.collections:
        patch.set_alpha(0.8)
    for cat, p_val, signif in category_results:
        plt.text(df[category_col].unique().tolist().index(cat), df[duration_col].max(), f'p={p_val:.4f}, {signif}', ha='center', color='crimson', alpha=0.7)
    plt.title('Violin Plot of Duration by Category and Experiment Period')
    plt.xlabel(category_col)
    plt.ylabel('Duration')
    plt.xticks(rotation=0)
    plt.legend(title=period_col)
    plt.savefig(output_file)

def plot_bar(df, category_col, period_col, duration_col, output_file, category_results):
    df_grouped = df.groupby([category_col, period_col])[duration_col].sum().reset_index()
    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid")
    palette = sns.color_palette("hls", len(df_grouped[category_col].unique()))
    bar_plot = sns.barplot(x=category_col, y=duration_col, hue=period_col, data=df_grouped, palette=palette, alpha=0.8)
    plt.title('Total Duration of Each Category for Each Period')
    for cat, p_val, signif in category_results:
        plt.text(df_grouped[category_col].unique().tolist().index(cat), df_grouped[duration_col].max(), f'p={p_val:.4f}, {signif}', ha='center', color='crimson', alpha=0.7)
    plt.xlabel(category_col)
    plt.ylabel('Total Duration')
    plt.xticks(rotation=0)
    plt.legend(title=period_col)
    plt.subplots_adjust(bottom=0.3)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)


df = pd.read_csv('../../data/csv/outlier_removed/device_outlier_removed.csv', dtype={'user': str})
df_1st_half = df[df['days'] == '1st_half']
df_2nd_half = df[df['days'] == '2nd_half']
print(df_1st_half['category'].value_counts(dropna=False))
print(df_2nd_half['category'].value_counts(dropna=False))
print(f"================================================\n")
category_results = []
for category in df['category'].unique():
    df1 = df_1st_half[df_1st_half['category'] == category]
    df2 = df_2nd_half[df_2nd_half['category'] == category]
    print(f"category: {category}")
    p_value, significance = compare_groups(df1, df2, 'duration')
    category_results.append((category, p_value, significance))

plot_bar(df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/barplot.png', category_results)
plot_boxplot(df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/boxplot.png', category_results)
plot_scatter(df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/scatterplot.png', category_results)
plot_violin(df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/violinplot.png', category_results)