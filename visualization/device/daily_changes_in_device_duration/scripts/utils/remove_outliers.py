import pandas as pd
import os

def remove_outliers_by_IQR(df, column_name):
    # Calculate the first and third quartiles
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)

    # Calculate the Interquartile Range (IQR)
    IQR = Q3 - Q1

    # Define outlier conditions
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Filter out the outliers
    filtered_df = df[(df[column_name] >= lower_bound) & (df[column_name] <= upper_bound)]

    return filtered_df

def identify_outliers_by_IQR(df, column_name):
    # Calculate the first and third quartiles
    Q1 = df[column_name].quantile(0.25)
    Q3 = df[column_name].quantile(0.75)

    # Calculate the Interquartile Range (IQR)
    IQR = Q3 - Q1

    # Define outlier conditions
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify outliers
    outlier_df = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)]

    return outlier_df

# Example usage
df = pd.read_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time.csv', dtype={'user': str})
print(df)

filtered_df = remove_outliers_by_IQR(df, 'viewing_time')
print(filtered_df)

outlier_df = identify_outliers_by_IQR(df, 'viewing_time')
print(outlier_df)


output_file1 = '../../data/csv/remove_outliers/device_add_days_viewing_time_del_outliers_iqr.csv'
os.makedirs(os.path.dirname(output_file1), exist_ok=True)
output_file2 = '../../data/csv/remove_outliers/device_add_days_viewing_time_outliers_iqr.csv'
os.makedirs(os.path.dirname(output_file2), exist_ok=True)

# Save the filtered data and outliers to separate files
filtered_df.to_csv(output_file1, index=False)
outlier_df.to_csv(output_file2, index=False)
