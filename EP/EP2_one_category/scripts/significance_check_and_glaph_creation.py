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
        test_name = "Shapiro-Wilk test "
    elif test_type == "ks":
        stat, p = stats.kstest(data, 'norm', args=(np.mean(data), np.std(data, ddof=1)))
        test_name = "Kolmogorov-Smirnov"
    result = "Normal" if p > 0.05 else "Not normal"
    print(f"{test_name}: p-value = {p:.18f} - {result}")
    return p > 0.05

def check_equal_variance(df1, df2, column, normal=True):
    if df1[column].empty or df2[column].empty or len(df1[column]) < 3 or len(df2[column]) < 3:
        return None
    if normal:
        stat, p = stats.levene(df1[column], df2[column])
        test_name = "Levene's test     "
    else:
        stat, p = stats.bartlett(df1[column], df2[column])
        test_name = "Brown-Forsythe    "
    result = "Equal variances" if p > 0.05 else "Unequal variances"
    print(f"{test_name}: p-value = {p:.18f} - {result}")
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
            test_type = "Paired t-test     "
        else:
            equal_var = check_equal_variance(df1, df2, column, normal=True)
            if equal_var:
                stat, p = stats.ttest_ind(df1[column], df2[column])
                test_type = "Independent t-test"
            else:
                stat, p = stats.ttest_ind(df1[column], df2[column], equal_var=False)
                test_type = "Welch's t-test    "
    else:
        equal_var = check_equal_variance(df1, df2, column, normal=False)
        if equal_var:
            stat, p = stats.mannwhitneyu(df1[column], df2[column])
            test_type = "Mann-Whitney U    "
        else:
            stat, p = stats.ranksums(df1[column], df2[column])
            test_type = "Wilcoxon rank-sum "
    significance = "Significant" if p < 0.05 else "Not significant"
    print(f"{test_type}: p-value = {p:.18f} - {significance}")
    return p, significance

def print_statistics(df, category_col, period_col, duration_col):
    statistics_df = df.groupby([category_col, period_col])[duration_col].agg(['mean', 'var', 'std']).reset_index()
    print(statistics_df)

def plot_boxplot(df, category_col, period_col, duration_col, output_file, category_results):
    categories = df[category_col].unique()
    n_categories = len(categories)
    n_cols = min(n_categories, 3)
    n_rows = (n_categories + 2) // 3
    fig_width = 18 if n_cols < 3 else 16
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(fig_width, 24), sharey=True)
    if n_rows == 1 and n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    for i, category in enumerate(categories):
        ax = axes[i]
        category_df = df[df[category_col] == category]
        sns.boxplot(x=category_col, y=duration_col, hue=period_col, data=category_df, ax=ax, palette="hls")
        ax.set_title(category)
        ax.set_xlabel('')
        ax.set_ylabel('Duration' if i % n_cols == 0 else '')
        cat_result = next((item for item in category_results if item[0] == category), None)
        if cat_result:
            text_color = 'crimson' if cat_result[2] == "Significant" else 'black'
            ax.text(0.5, 0.90, f'p={cat_result[1]:.4f}, {cat_result[2]}', ha='center', transform=ax.transAxes, color=text_color, alpha=0.7, fontsize=18)
    plt.suptitle('Boxplot of Duration by Category and Experiment Period')
    handles, labels = ax.get_legend_handles_labels()
    for ax in axes:
        if ax.get_legend() is not None:
            ax.get_legend().remove()
    axes = axes.flatten()
    fig.legend(handles, labels, title=period_col, loc='upper right', bbox_to_anchor=(0.99, 0.99), borderaxespad=0.)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)

def plot_scatter(df, category_col, period_col, duration_col, output_file, category_results):
    categories = df[category_col].unique()
    periods = df[period_col].unique().tolist()
    n_categories = len(categories)
    n_periods = len(periods)
    n_cols = min(n_categories, 3)
    n_rows = (n_categories + 2) // 3
    fig_width = 18 if n_cols < 3 else 16
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(fig_width, 24), sharey=True)
    if n_rows == 1 and n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    x_points = {period: i * 0.5 for i, period in enumerate(periods)}
    for i, category in enumerate(categories):
        ax = axes[i]
        category_df = df[df[category_col] == category]
        for period in periods:
            period_df = category_df[category_df[period_col] == period]
            ax.scatter(np.full(len(period_df), x_points[period]), period_df[duration_col], alpha=0.5, label=period)
        ax.set_title(category)
        ax.set_ylabel('Duration' if i % n_cols == 0 else '')
        ax.set_xticks(list(x_points.values()))
        ax.set_xticklabels(periods)
        ax.set_xlabel('')

        cat_result = next((item for item in category_results if item[0] == category), None)
        if cat_result:
            text_color = 'crimson' if cat_result[2] == "Significant" else 'black'
            ax.text(0.5, 0.90, f'p={cat_result[1]:.4f}, {cat_result[2]}', ha='center', transform=ax.transAxes, color=text_color, alpha=0.7, fontsize=18)
    plt.suptitle('Scatter Plot of Duration for Each Category by Period')
    for ax in axes:
        if ax.get_legend() is not None:
            ax.get_legend().remove()
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, title=period_col, loc='upper right', bbox_to_anchor=(0.99, 0.99), borderaxespad=0.)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)

def plot_violin(df, category_col, period_col, duration_col, output_file, category_results):
    categories = df[category_col].unique()
    n_categories = len(categories)
    n_cols = min(n_categories, 3)
    n_rows = (n_categories + 2) // 3
    fig_width = 18 if n_cols < 3 else 16
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(fig_width, 24), sharey=True)
    if n_rows == 1 and n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    for i, category in enumerate(categories):
        ax = axes[i]
        category_df = df[df[category_col] == category]
        sns.violinplot(x=category_col, y=duration_col, hue=period_col, data=category_df, ax=ax, palette="hls", split=True)
        for patch in ax.collections:
            patch.set_alpha(0.8)
        ax.set_title(category)
        ax.set_xlabel('')
        ax.set_ylabel('Duration' if i % n_cols == 0 else '')
        cat_result = next((item for item in category_results if item[0] == category), None)
        if cat_result:
            text_color = 'crimson' if cat_result[2] == "Significant" else 'black'
            ax.text(0.5, 0.90, f'p={cat_result[1]:.4f}, {cat_result[2]}', ha='center', transform=ax.transAxes, color=text_color, alpha=0.7, fontsize=18)
    plt.suptitle('Violin Plot of Duration by Category and Experiment Period')
    handles, labels = axes[0].get_legend_handles_labels()
    for ax in axes:
        if ax.get_legend() is not None:
            ax.get_legend().remove()
    fig.legend(handles, labels, title=period_col, loc='upper right', bbox_to_anchor=(0.99, 0.99), borderaxespad=0.)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)

def plot_bar(df, category_col, period_col, duration_col, output_file, category_results):
    categories = df[category_col].unique()
    n_categories = len(categories)
    n_cols = min(n_categories, 3)
    n_rows = (n_categories + 2) // 3
    fig_width = 18 if n_cols < 3 else 16
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(fig_width, 24), sharey=True)
    if n_rows == 1 and n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    for i, category in enumerate(categories):
        ax = axes[i]
        category_df = df[df[category_col] == category]
        sns.barplot(x=category_col, y=duration_col, hue=period_col, data=category_df, ax=ax, palette="hls", alpha=0.8, errorbar=None)
        ax.set_title(category)
        ax.set_xlabel('')
        ax.set_ylabel('Total Duration' if i % n_cols == 0 else '')
        cat_result = next((item for item in category_results if item[0] == category), None)
        if cat_result:
            text_color = 'crimson' if cat_result[2] == "Significant" else 'black'
            ax.text(0.5, 0.90, f'p={cat_result[1]:.4f}, {cat_result[2]}', ha='center', transform=ax.transAxes, color=text_color, alpha=0.7, fontsize=18)
    plt.suptitle('Total Duration of Each Category for Each Period')
    handles, labels = axes[0].get_legend_handles_labels()
    for ax in axes:
        if ax.get_legend() is not None:
            ax.get_legend().remove()
    fig.legend(handles, labels, title=period_col, loc='upper right', bbox_to_anchor=(0.99, 0.99), borderaxespad=0.)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)

def plot_histograms(df, category_col, period_col, duration_col, output_file):
    categories = df[category_col].unique()
    periods = df[period_col].unique()
    n_rows = -(-len(categories) // 2)
    n_cols = len(periods) * 2
    fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(n_cols*3, n_rows*4), sharex=True, sharey=True)
    if n_rows == 1 and n_cols == 1:
        axes = np.array([axes])
    axes = axes.flatten()
    for i, category in enumerate(categories):
        row = i // 2
        col = i % 2 * len(periods)
        for j, period in enumerate(periods):
            ax = axes[row * n_cols + col + j]
            subset = df[(df[category_col] == category) & (df[period_col] == period)]
            n_data_points = len(subset)
            bin_nums = 1 + int(np.log2(n_data_points)) if n_data_points > 0 else 1
            sns.histplot(subset[duration_col], kde=True, ax=ax, bins=bin_nums, color='skyblue', alpha=0.8)
            ax.set_title(f'{category} - {period}')
            ax.set_xlabel(duration_col if row == n_rows - 1 else '')
            ax.set_ylabel('Frequency' if col == 0 else '')
    plt.tight_layout()
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    plt.savefig(output_file)


input_file_path = '../data/csv/complete/TV.csv'
base = os.path.basename(input_file_path)
filename, _ = os.path.splitext(base)
output_folder = f'../data/img/{filename}'

df = pd.read_csv(input_file_path, dtype={'user': str})
df_EP1 = df[df['period'] == 'EP1']
df_EP2 = df[df['period'] == 'EP2']
combined_df = pd.concat([df_EP1, df_EP2]).reset_index(drop=True)
print(combined_df)
print(df_EP1['category'].value_counts(dropna=False))
print(df_EP2['category'].value_counts(dropna=False))
print(f"================================================")

print("\n統計量（'category', 'period'）：")
print_statistics(combined_df, 'category', 'period', 'duration')

category_results = []
for category in df['category'].unique():
    ep1 = df_EP1[df_EP1['category'] == category]
    ep2 = df_EP2[df_EP2['category'] == category]
    print(f"\ncategory: {category}")
    result = compare_groups(ep1, ep2, 'duration', paired=True)
    if result is not None:
        p_value, significance = result
        category_results.append((category, p_value, significance))
    else:
        print("Unable to perform statistical test because data is less than 3.")

plot_bar(combined_df, 'category', 'period', 'duration', f'{output_folder}/barplot.png', category_results)
plot_boxplot(combined_df, 'category', 'period', 'duration', f'{output_folder}/boxplot.png', category_results)
plot_scatter(combined_df, 'category', 'period', 'duration', f'{output_folder}/scatterplot.png', category_results)
plot_violin(combined_df, 'category', 'period', 'duration', f'{output_folder}/violinplot.png', category_results)
plot_histograms(combined_df, 'category', 'period', 'duration', f'{output_folder}/histogram.png')
plt.close('all')