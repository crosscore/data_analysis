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
    return p

def plot_boxplot(df, category_col, period_col, duration_col, output_file):
    plt.figure(figsize=(12, 8))
    ax = sns.boxplot(x=category_col, y=duration_col, hue=period_col, data=df, palette="hls")
    # ボックスの本体に透明度を設定
    for patch in ax.artists:
        patch.set_alpha(0.8)
    # ヒゲ、キャップ、アウトライヤーに透明度を設定
    for line in ax.lines:
        line.set_alpha(0.8)
    plt.title('Boxplot of Duration by Category and Experiment Period')
    plt.xlabel(category_col)
    plt.ylabel('Duration')
    plt.xticks(rotation=0)
    plt.legend(title=period_col)
    plt.savefig(output_file)

def plot_scatter(df, category_col, period_col, duration_col, output_file):
    plt.figure(figsize=(12, 8))
    categories = df[category_col].unique()
    periods = df[period_col].unique()
    palette = sns.color_palette("hls", len(categories))
    period_indices = {period: index for index, period in enumerate(periods)}
    offset = np.linspace(-0.2, 0.2, len(categories))
    # Settings to add jitter
    jitter_amount = 0.15
    for category, color, off in zip(categories, palette, offset):
        for period in periods:
            period_index = period_indices[period]
            category_df = df[(df[category_col] == category) & (df[period_col] == period)]
            if not category_df.empty:
                # Add jitter and adjust alpha value and data point size
                jittered_x = period_index + off + np.random.uniform(-jitter_amount, jitter_amount, size=category_df.shape[0])
                plt.scatter(jittered_x, category_df[duration_col], color=color, alpha=0.5, s=10, label=f'{category} ({period})')
    plt.title('Scatter Plot of Duration for Each Category by Period')
    plt.xlabel(period_col)
    plt.ylabel(duration_col)
    plt.legend(title=category_col, loc='upper right', bbox_to_anchor=(1.3, 1))
    plt.xticks(ticks=np.arange(len(periods)), labels=periods)
    plt.subplots_adjust(right=0.8)
    plt.savefig(output_file)

def plot_violin(df, category_col, period_col, duration_col, output_file):
    plt.figure(figsize=(12, 8))
    ax = sns.violinplot(x=category_col, y=duration_col, hue=period_col, data=df, palette="hls", split=True)
    for patch in ax.collections:
        patch.set_alpha(0.8)
    plt.title('Violin Plot of Duration by Category and Experiment Period')
    plt.xlabel(category_col)
    plt.ylabel('Duration')
    plt.xticks(rotation=0)
    plt.legend(title=period_col)
    plt.savefig(output_file)

def plot_bar(df, category_col, period_col, duration_col, output_file, significant_categories):
    df_grouped = df.groupby([category_col, period_col])[duration_col].sum().reset_index()
    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid")
    palette = sns.color_palette("hls", len(df_grouped[category_col].unique()))
    bar_plot = sns.barplot(x=category_col, y=duration_col, hue=period_col, data=df_grouped, palette=palette, alpha=0.8)
    plt.title('Total Duration of Each Category for Each Period')
    plt.xlabel(category_col)
    plt.ylabel('Total Duration')
    plt.xticks(rotation=0)
    plt.legend(title=period_col)
    plt.subplots_adjust(bottom=0.3)
    # Highlight labels of categories with significant differences
    for label in bar_plot.get_xticklabels():
        if label.get_text() in significant_categories:
            label.set_color('crimson')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)


df = pd.read_csv('../data/csv/outlier_removed/device_outlier_removed.csv', dtype={'user': str})
df_1st_half = df[df['days'] == '1st_half']
df_2nd_half = df[df['days'] == '2nd_half']
print(df_1st_half['category'].value_counts(dropna=False))
print(df_2nd_half['category'].value_counts(dropna=False))
print(f"================================================\n")
results = {}
significance_level = 0.05
for category in df['category'].unique():
    df1 = df_1st_half[df_1st_half['category'] == category]
    df2 = df_2nd_half[df_2nd_half['category'] == category]
    print(f"category: {category}")
    p_value = compare_groups(df1, df2, 'duration')

# Create a list of categories judged to be significant differences
significant_categories = [category for category, (result, _) in results.items() if "Significant difference" in result]

# Generate and save bar plot
plot_bar(df, 'category', 'days', 'duration', '../data/img/device_soft_and_hard_2exp/barplot.png', significant_categories)

# Generate and save boxplot
plot_boxplot(df, 'category', 'days', 'duration', '../data/img/device_soft_and_hard_2exp/boxplot.png')

# Generate and save scatter plot
plot_scatter(df, 'category', 'days', 'duration', '../data/img/device_soft_and_hard_2exp/scatterplot.png')

# Generate and save violin plot
plot_violin(df, 'category', 'days', 'duration', '../data/img/device_soft_and_hard_2exp/violinplot.png')