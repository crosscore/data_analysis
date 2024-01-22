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
    if len(data) < 3:
        print("Data length is less than 3, returning original data.")
        return data
    
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
        if not filtered_data.empty:
            results.append(subset.loc[filtered_data.index])
    if results:
        return pd.concat(results)
    else:
        return pd.DataFrame()

df = pd.read_csv('../../data/csv/date_range/TV_date_range.csv', dtype={'user': str})
print(df)
print(df['tv_category'].value_counts(dropna=False))

# Split data based on experiment period
exp1_range = pd.to_datetime(['2022-10-22', '2022-11-04'])
df['date'] = pd.to_datetime(df['date'])
df_exp1 = df[df['date'].between(exp1_range[0], exp1_range[1])]
df_exp2 = df[~df['date'].between(exp1_range[0], exp1_range[1])]
print(df_exp1)
print(df_exp2)

processed_df_exp1 = process_data(df_exp1, category='tv_category')
processed_df_exp2 = process_data(df_exp2, category='tv_category')
processed_df = pd.concat([processed_df_exp1, processed_df_exp2])

output_file = '../../data/csv/outlier_removed/TV_outlier_removed.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
print(processed_df)
print(processed_df['tv_category'].value_counts(dropna=False))
processed_df.to_csv(output_file, index=False)