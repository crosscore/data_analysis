import pandas as pd

df = pd.read_csv('../../data/csv/original/all_device.csv', dtype={'user': str})
print(df)

# Display the number of each category column in df (including nan values)
#print(df['category'].value_counts(dropna=False))

#df[df['category'].isna()].to_csv('../../data/csv/add_category/category_nan_row.csv', index=False)

# Convert 'start_viewing_date' and 'stop_viewing_date' to datetime
df['start_viewing_date'] = pd.to_datetime(df['start_viewing_date'])
df['stop_viewing_date'] = pd.to_datetime(df['stop_viewing_date'])

# Filter rows where 'start_viewing_date' is later than 'stop_viewing_date'
invalid_rows = df[(df['start_viewing_date'] > df['stop_viewing_date'])]
normal_rows = df[~(df['start_viewing_date'] > df['stop_viewing_date'])]

invalid_rows.to_csv('../../data/csv/original/all_device_invalid_time.csv', index=False)
normal_rows.to_csv('../../data/csv/original/all_device_normal.csv', index=False)