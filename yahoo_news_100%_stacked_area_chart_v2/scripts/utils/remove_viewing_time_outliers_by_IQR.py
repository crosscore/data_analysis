import pandas as pd

df = pd.read_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time.csv', dtype={'user': str})
print(df)

# Calculate the first and third quartiles of the 'viewing_time' column
Q1 = df['viewing_time'].quantile(0.25)
Q3 = df['viewing_time'].quantile(0.75)

# Calculate the Interquartile Range (IQR)
IQR = Q3 - Q1

# Define outlier conditions (outside Q1 - 1.5 * IQR and Q3 + 1.5 * IQR)
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
filtered_df = df[(df['viewing_time'] >= lower_bound) & (df['viewing_time'] <= upper_bound)]
print(filtered_df)

# Identify outliers
outlier_df = df[(df['viewing_time'] < lower_bound) | (df['viewing_time'] > upper_bound)]
print(outlier_df)

filtered_df.to_csv('../../data/csv/remove_outliers/iqr/device_add_days_viewing_time_del_outliers_iqr.csv', index=False)
outlier_df.to_csv('../../data/csv/remove_outliers/iqr/device_add_days_viewing_time_outliers_iqr.csv', index=False)
