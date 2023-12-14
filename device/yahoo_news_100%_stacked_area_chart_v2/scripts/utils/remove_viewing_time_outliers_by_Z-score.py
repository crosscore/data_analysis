import pandas as pd

df = pd.read_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time.csv', dtype={'user': str})
print(df)

# Calculate the mean and standard deviation of the 'viewing_time' column
mean = df['viewing_time'].mean()
std = df['viewing_time'].std()

# Define outlier conditions (mean ± 3 * standard deviation)
lower_bound = mean - 2 * std
upper_bound = mean + 2 * std

# remove outliers
filtered_df = df[(df['viewing_time'] >= lower_bound) & (df['viewing_time'] <= upper_bound)]
print(filtered_df)

outlier_df = df[(df['viewing_time'] < lower_bound) | (df['viewing_time'] > upper_bound)]
print(outlier_df)

filtered_df.to_csv('../../data/csv/remove_outliers/device_add_days_viewing_time_del_outliers.csv', index=False)
outlier_df.to_csv('../../data/csv/remove_outliers/device_add_days_viewing_time_outliers.csv', index=False)
