import pandas as pd
from itertools import product

df = pd.read_csv("../../data/csv/original/device.csv", dtype={'user': str})

df['category'] = pd.to_datetime(df['date']).dt.strftime('%H')
df = df.groupby(['user', 'category', 'period'])['duration'].sum().reset_index()

all_users = df['user'].unique()
all_periods = df['period'].unique()
all_categories = [f'{hour:02d}' for hour in range(24)]

all_combinations = pd.DataFrame(product(all_users, all_categories, all_periods), columns=['user', 'category', 'period'])

df_full = pd.merge(all_combinations, df, on=['user', 'category', 'period'], how='left').fillna(0)
df_full['duration'] = df_full['duration'].astype(int)

df_full = df_full.sort_values(['period', 'user', 'category'])
print(df_full)

df_full.to_csv("../../data/csv/complete/device.csv", index=False)
