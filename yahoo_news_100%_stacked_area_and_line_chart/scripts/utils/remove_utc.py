import pandas as pd

df = pd.read_csv('../../data/csv/device_with_category.csv', dtype={'user': str})

# 各列に含まれる'+09:00'を取り除く
df['start_viewing_date'] = df['start_viewing_date'].str.replace('+09:00', '')
df['stop_viewing_date'] = df['stop_viewing_date'].str.replace('+09:00', '')
df['eliminate_date'] = df['eliminate_date'].str.replace('+09:00', '')
df['base_date'] = df['base_date'].str.replace('+09:00', '')

df.to_csv('../../data/csv/device_with_category_remove_utc.csv', index=False)
