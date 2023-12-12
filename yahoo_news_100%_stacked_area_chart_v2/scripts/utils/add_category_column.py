import pandas as pd

# Load the CSV files
all_device_df = pd.read_csv('../../data/csv/original/all_device.csv', dtype={'user': str})
device_with_category_df = pd.read_csv('../../data/csv/original/device_with_category_v3.csv', dtype={'user': str})

# Ensure that 'category' column exists in all_device_df
if 'category' not in all_device_df.columns:
    all_device_df['category'] = None

# Merge the 'category' data from device_with_category_df into all_device_df
all_device_df = all_device_df.merge(device_with_category_df[['url', 'category']], on='url', how='left')

# If there are any duplicate columns (e.g., 'category_x', 'category_y'), 
# combine them and drop the unnecessary ones
if 'category_x' in all_device_df.columns and 'category_y' in all_device_df.columns:
    all_device_df['category'] = all_device_df['category_y'].fillna(all_device_df['category_x'])
    all_device_df.drop(['category_x', 'category_y'], axis=1, inplace=True)

# Save the updated dataframe to a new CSV file
all_device_df.to_csv('../../data/csv/add_category/all_device_add_category.csv', index=False)
