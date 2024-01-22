import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from scipy import stats

# Function to unify time format
def unify_time_format(time_str):
    # Split the time string by colon
    parts = time_str.split(':')

    # If there are only two parts (hours and minutes), add ":00" for seconds
    if len(parts) == 2:
        return time_str + ":00"
    return time_str

def test_normality_shapiro_wilk(data):
    """
    Perform the Shapiro-Wilk test for normality.
    """
    stat, p_value = stats.shapiro(data)
    print(f'Shapiro-Wilk Test: Statistics={stat}, p-value={p_value}')

    if p_value > 0.05:
        print('Sample looks Gaussian (fail to reject H0)')
    else:
        print('Sample does not look Gaussian (reject H0)')

def test_normality_ks(data, source_name):
    """
    Perform the Kolmogorov-Smirnov test for normality.
    """
    # KS test for normality
    d, p_value = stats.kstest(data, 'norm', args=(data.mean(), data.std()))
    print(f'Kolmogorov-Smirnov Test for {source_name}: D={d}, p-value={p_value}')

    if p_value > 0.05:
        print(f'{source_name}: Sample looks Gaussian (fail to reject H0)')
    else:
        print(f'{source_name}: Sample does not look Gaussian (reject H0)')

def perform_ttest_by_source(df1, df2):
    """
    Perform t-test for each source name and print the result in English.
    """
    df1 = df1.copy()
    df2 = df2.copy()
    df1['experiment'] = 'exp1'
    df2['experiment'] = 'exp2'
    combined_df = pd.concat([df1, df2])

    # Group by source name and perform t-test
    ttest_results = []
    for source_name in combined_df['source_name'].unique():
        duration_exp1 = combined_df[(combined_df['source_name'] == source_name) & (combined_df['experiment'] == 'exp1')]['duration']
        duration_exp2 = combined_df[(combined_df['source_name'] == source_name) & (combined_df['experiment'] == 'exp2')]['duration']

        t_stat, p_value = stats.ttest_ind(duration_exp1, duration_exp2, equal_var=False)  # Welch's t-test
        ttest_results.append({'source_name': source_name, 't_stat': t_stat, 'p_value': p_value})

        # Check if p-value is less than 0.05 and print the result in English
        if p_value < 0.05:
            print(f"There is a significant difference: {source_name} (p-value = {p_value:.15f})")
        else:
            print(f"There is no significant difference: {source_name} (p-value = {p_value:.15f})")

    return pd.DataFrame(ttest_results)

def perform_mannwhitneyu_test_by_source(df1, df2):
    """
    Perform Mann-Whitney U test for each source name and print the result in English.
    """
    mwu_results = []
    for source_name in pd.concat([df1, df2])['source_name'].unique():
        duration_exp1 = df1[df1['source_name'] == source_name]['duration']
        duration_exp2 = df2[df2['source_name'] == source_name]['duration']

        # Perform Mann-Whitney U test
        u_stat, p_value = stats.mannwhitneyu(duration_exp1, duration_exp2, alternative='two-sided')

        mwu_results.append({'source_name': source_name, 'U_stat': u_stat, 'p_value': p_value})

        # Check if p-value is less than 0.05 and print the result in English
        if p_value < 0.05:
            print(f"There is a significant difference: {source_name} (p-value = {p_value:.15f})")
        else:
            print(f"There is no significant difference: {source_name} (p-value = {p_value:.15f})")

    return pd.DataFrame(mwu_results)

def plot_total_duration_comparison(df1, df2, title):
    # Calculate total duration for each source name in each dataset
    total_duration_df1 = df1.groupby('source_name')['duration'].sum().reset_index()
    total_duration_df2 = df2.groupby('source_name')['duration'].sum().reset_index()

    # Merge the two dataframes for comparison
    merged_df = pd.merge(total_duration_df1, total_duration_df2, on='source_name', suffixes=('_exp1', '_exp2'))
    print(merged_df)

    # Melting the dataframe for easier plotting
    melted_df = pd.melt(merged_df, id_vars='source_name', var_name='experiment', value_name='total_duration')

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='source_name', y='total_duration', hue='experiment', data=melted_df)
    plt.title(title)
    plt.xlabel('Source Name')
    plt.ylabel('Total Duration')
    plt.xticks(rotation=270)
    plt.tight_layout()

    # Save plot
    file_name = 'total_duration_comparison.png'
    output_path = f'../../data/img/duration_comparison/all/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    print(f'{output_path} output completed.')

# Load dataset
df = pd.read_csv('../../data/csv/concat_and_IQR/MBapp_TV_with_category.csv', dtype={'user': str})
#print(df)

# Apply the function to the 'time' column (replace 'time' with the actual name of your time column)
df['date'] = df['date'].apply(unify_time_format)

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d %H:%M:%S', dayfirst=True)

# Split the data into two dataframes based on the specified date range
start_date = '2022-10-22'
end_date = '2022-11-04'
df_exp1 = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
df_exp2 = df[(df['date'] < start_date) | (df['date'] > end_date)]

print("\n====== exec Shapiro-Wilk Test ======")
print("Normality Test for Experiment Period 1:")
for source_name in df_exp1['source_name'].unique():
    data = df_exp1[df_exp1['source_name'] == source_name]['duration']
    print(f"Testing normality for {source_name} in Experiment Period 1:")
    test_normality_shapiro_wilk(data)

print("\nNormality Test for Experiment Period 2:")
for source_name in df_exp2['source_name'].unique():
    data = df_exp2[df_exp2['source_name'] == source_name]['duration']
    print(f"Testing normality for {source_name} in Experiment Period 2:")
    test_normality_shapiro_wilk(data)

print("\n====== exec Kolomogorov-Smirnov Test ======")
print("Kolmogorov-Smirnov Test for Experiment Period 1:")
for source_name in df_exp1['source_name'].unique():
    data = df_exp1[df_exp1['source_name'] == source_name]['duration']
    print(f"Testing normality (KS) for {source_name} in Experiment Period 1:")
    test_normality_ks(data, source_name)

print("\nKolmogorov-Smirnov Test for Experiment Period 2:")
for source_name in df_exp2['source_name'].unique():
    data = df_exp2[df_exp2['source_name'] == source_name]['duration']
    print(f"Testing normality (KS) for {source_name} in Experiment Period 2:")
    test_normality_ks(data, source_name)

# Perform t-test for each source
print("\n====== exec perform_ttest_by_source ======")
ttest_results_df = perform_ttest_by_source(df_exp1, df_exp2)
print("T-test results by source name:")
print(ttest_results_df)

# Apply the Mann-Whitney U test function
print("\n====== Exec perform_mannwhitneyu_test_by_source ======")
mwu_test_results_df = perform_mannwhitneyu_test_by_source(df_exp1, df_exp2)
print("Mann-Whitney U test results by source name:")
print(mwu_test_results_df)

# Plot and save the comparison graph
plot_total_duration_comparison(df_exp1, df_exp2, 'Total Duration Comparison Between Experiments')
