#significance_check_and_glaph_creation.py
import pandas as pd
import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import os

def is_normal(data, test_type="shapiro"):
    if len(data) < 3:
        return False
    if test_type == "shapiro":
        stat, p = stats.shapiro(data)
        test_name = "Shapiro-Wilk"
    elif test_type == "ks":
        stat, p = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data, ddof=1)))
        test_name = "Kolmogorov-Smirnov"
    result = "Normal" if p > 0.05 else "Not normal"
    print(f"{test_name}: {result}")
    return p > 0.05

def check_equal_variance(df1, df2, column, normal=True):
    if df1[column].empty or df2[column].empty or len(df1[column]) < 3 or len(df2[column]) < 3:
        return None
    if normal:
        stat, p = stats.levene(df1[column], df2[column])
        test_name = "Levene's"
    else:
        stat, p = stats.bartlett(df1[column], df2[column])
        test_name = "Brown-Forsythe"
    result = "Equal variances" if p > 0.05 else "Unequal variances"
    print(f"{test_name} test: {result}")
    return p > 0.05

def compare_groups(df1, df2, column, paired=True):
    if df1[column].empty or df2[column].empty or len(df1[column]) < 3 or len(df2[column]) < 3:
        return None
    if paired and len(df1[column]) != len(df2[column]):
        paired = False
    normal_test_type = "shapiro" if len(df1[column]) < 5000 else "ks"
    df1_normal = is_normal(df1[column], normal_test_type)
    df2_normal = is_normal(df2[column], normal_test_type)
    test_type = ""
    if df1_normal and df2_normal:
        if paired:
            stat, p = stats.ttest_rel(df1[column], df2[column])
            test_type = "Paired t-test"
        else:
            equal_var = check_equal_variance(df1, df2, column, normal=True)
            if equal_var:
                stat, p = stats.ttest_ind(df1[column], df2[column])
                test_type = "Independent t-test"
            else:
                stat, p = stats.ttest_ind(df1[column], df2[column], equal_var=False)
                test_type = "Welch's t-test"
    else:
        equal_var = check_equal_variance(df1, df2, column, normal=False)
        if equal_var:
            stat, p = stats.mannwhitneyu(df1[column], df2[column])
            test_type = "Mann-Whitney U"
        else:
            stat, p = stats.ranksums(df1[column], df2[column])
            test_type = "Wilcoxon rank-sum"
    significance = "Significant" if p < 0.05 else "Not significant"
    print(f"{test_type}: p-value = {p:.18f} - {significance}")
    return p, significance

def print_statistics(df, category_col, period_col, duration_col):
    statistics_df = df.groupby([category_col, period_col])[duration_col].agg(['mean', 'var', 'std']).reset_index()
    print(statistics_df)

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
    jitter_amount = 0.04
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

def plot_histograms_by_category_and_days(df, category_col, period_col, duration_col, output_file):
    categories = df[category_col].unique()
    periods = df[period_col].unique()
    nrows = len(categories)
    ncols = len(periods)
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*6, nrows*4))
    for i, category in enumerate(categories):
        for j, period in enumerate(periods):
            ax = axes[i, j]
            subset = df[(df[category_col] == category) & (df[period_col] == period)]
            sns.histplot(subset[duration_col], kde=True, ax=ax, bins=20, color='skyblue', alpha=0.8)
            ax.set_title(f'{category} - {period}')
            ax.set_xlabel(duration_col)
            ax.set_ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(output_file)

df = pd.read_csv('../../data/csv/outlier_removed/device_outlier_removed.csv', dtype={'user': str})
grouped_df = df.groupby(['user', 'category', 'days'])['duration'].sum().reset_index()
df_1st_half_sum = grouped_df[grouped_df['days'] == '1st_half']
df_2nd_half_sum = grouped_df[grouped_df['days'] == '2nd_half']
combined_df = pd.concat([df_1st_half_sum, df_2nd_half_sum]).reset_index(drop=True)
print(combined_df)
print(df_1st_half_sum['category'].value_counts(dropna=False))
print(df_2nd_half_sum['category'].value_counts(dropna=False))
print(f"================================================")

print("\n統計量（'category', 'days'）：")
print_statistics(combined_df, 'category', 'days', 'duration')

category_results = []
for category in df['category'].unique():
    df1 = df_1st_half_sum[df_1st_half_sum['category'] == category]
    df2 = df_2nd_half_sum[df_2nd_half_sum['category'] == category]
    print(f"\ncategory: {category}")
    p_value, significance = compare_groups(df1, df2, 'duration', paired=True)
    category_results.append((category, p_value, significance))

plot_bar(combined_df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/barplot.png', category_results)
plot_boxplot(combined_df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/boxplot.png', category_results)
plot_scatter(combined_df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/scatterplot.png', category_results)
plot_violin(combined_df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/violinplot.png', category_results)
plot_histograms_by_category_and_days(combined_df, 'category', 'days', 'duration', '../../data/img/device_soft_and_hard_2exp/histogram.png')
plt.close('all')