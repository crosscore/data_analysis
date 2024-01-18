import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

def is_normal_shapiro(data):
    print("Performing the Shapiro-Wilk test to check for normality. (< 5000 data points)")
    if np.ptp(data) == 0:
        print("Data range is zero, skipping the test.")
        return False
    stat, p = stats.shapiro(data)
    return p > 0.05

def is_normal_ks(data):
    print("Performing the Kolmogorov-Smirnov test to check for normality in a larger sample.")
    _, p = stats.kstest(data, 'norm')
    return p > 0.05

def remove_outliers(df, column):
    data = df[column]
    if len(data) < 3:
        print("Data length is less than 3, returning original data.")
        return df
    if len(data) < 5000:
        normal = is_normal_shapiro(data)
    else:
        print("Large sample size, skipping normality test.")
        normal = False
    if normal:
        print(f"Normal distribution. Applying 3σ Outlier Removal.")
        mean = np.mean(data)
        std = np.std(data)
        outliers = np.abs(data - mean) > 2 * std
    else:
        print(f"Not normal. Applying 3.0 IQR Outlier Removal.")
        q1 = np.percentile(data, 25)
        q3 = np.percentile(data, 75)
        iqr = q3 - q1
        lower_bound = q1 - 2.0 * iqr
        upper_bound = q3 + 2.0 * iqr
        outliers = (data < lower_bound) | (data > upper_bound)
    return df[~outliers]

input_folder = '../data/csv/add_weekdays/'
output_folder = '../data/csv/outlier_removed2/'
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        input_file_name = os.path.join(input_folder, file)

        df = pd.read_csv(input_file_name, dtype={'user': str})
        print(df)
        print(df['category'].value_counts(dropna=False))
        print(f"================================================")

        grouped = df.groupby(['user', 'category'])
        df = grouped.apply(lambda x: remove_outliers(x, 'duration')).reset_index(drop=True)

        base = os.path.basename(input_file_name)
        filename, ext = os.path.splitext(base)
        output_file = os.path.join(output_folder, f'{filename}.csv')

        print(f"\n================================================\n")
        print(df)
        print(df['category'].value_counts(dropna=False))

        df = df.sort_values(by=['period', 'user', 'date', 'category'])
        df.to_csv(output_file, index=False)