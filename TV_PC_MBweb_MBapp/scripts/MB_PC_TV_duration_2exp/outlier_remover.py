import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

def is_normal_shapiro(data):
    stat, p = stats.shapiro(data)
    return p > 0.05

def is_normal_ks(data):
    _, p = stats.kstest(data, 'norm')
    return p > 0.05

def remove_outliers(data, normal_test='shapiro'):
    if normal_test == 'shapiro':
        print(f'apply {normal_test}')
        normal = is_normal_shapiro(data)
    else:
        print(f'apply {normal_test}')
        normal = is_normal_ks(data)

    if normal:
        print(f"Applying normal distribution outlier removal.")
        mean = np.mean(data)
        std = np.std(data)
        return data[np.abs(data - mean) <= 2 * std]
    else:
        print(f"Not a normal distribution. Applying IQR outlier removal.")
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        return data[(data >= lower_bound) & (data <= upper_bound)]

def process_data(df, category, column='duration'):
    results = []
    for group in df[category].unique():
        print(f'Execute for {group}')
        subset = df[df[category] == group]
        data = subset[column]
        normal_test = 'shapiro' if len(data) < 5000 else 'ks'
        filtered_data = remove_outliers(data, normal_test)
        results.append(subset.loc[filtered_data.index])
    return pd.concat(results)

df = pd.read_csv('../../data/csv/concat/MBapp_MBweb_PC_TV.csv', dtype={'user': str})
print(df)
# Split data based on experiment period
start_date_exp1 = '2022-10-22'
end_date_exp1 = '2022-11-04'
df_exp1 = df[(df['date'] >= start_date_exp1) & (df['date'] <= end_date_exp1)]
df_exp2 = df[(df['date'] < start_date_exp1) | (df['date'] > end_date_exp1)]

processed_df_exp1 = process_data(df_exp1, category='source_name')
processed_df_exp2 = process_data(df_exp2, category='source_name')
processed_df = pd.concat([processed_df_exp1, processed_df_exp2])
output_file = '../../data/csv/outlier_removed/MBapp_MBweb_PC_TV_outlier_removed.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
processed_df.to_csv(output_file, index=False)
print(processed_df)
