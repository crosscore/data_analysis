import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

def is_normal_shapiro(data):
    print("Performing the Shapiro-Wilk test to check for normality. (< 5000 data points)")
    stat, p = stats.shapiro(data)
    return p > 0.05

def is_normal_ks(data):
    print("Performing the Kolmogorov-Smirnov test to check for normality in a larger sample.")
    _, p = stats.kstest(data, 'norm')
    return p > 0.05

def remove_outliers(data, normal_test='shapiro'):
    if len(data) < 3:
        print("Data length is less than 3, returning original data.")
        return data
    
    if normal_test == 'shapiro':
        normal = is_normal_shapiro(data)
    else:
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
        print(f'\nExecute for {group}')
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

df = pd.read_csv('../../data/csv/add_duration/device_add_duration.csv', dtype={'user': str})
print(df)
print(df['category'].value_counts(dropna=False))
print(f"================================================")
df_1st_half = df[df['days'] == '1st_half']
df_2nd_half = df[df['days'] == '2nd_half']

processed_df_1st_half = process_data(df_1st_half, category='category')
processed_df_2nd_half = process_data(df_2nd_half, category='category')
processed_df = pd.concat([processed_df_1st_half, processed_df_2nd_half])

output_file = '../../data/csv/outlier_removed/device_outlier_removed.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
print(f"\n================================================\n")
print(processed_df)
print(processed_df['category'].value_counts(dropna=False))
processed_df.to_csv(output_file, index=False)