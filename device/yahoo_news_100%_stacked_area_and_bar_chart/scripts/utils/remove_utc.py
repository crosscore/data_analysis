import pandas as pd

df = pd.read_csv('../../data/csv/device_with_category.csv', dtype={'user': str})

# Remove '+09:00' included in each column
df['start_viewing_date'] = df['start_viewing_date'].str.replace('+09:00', '')
df['stop_viewing_date'] = df['stop_viewing_date'].str.replace('+09:00', '')
df['eliminate_date'] = df['eliminate_date'].str.replace('+09:00', '')
df['base_date'] = df['base_date'].str.replace('+09:00', '')

df.to_csv('../../data/csv/device_with_category_remove_utc.csv', index=False)
