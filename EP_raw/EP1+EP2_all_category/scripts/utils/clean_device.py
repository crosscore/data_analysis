import pandas as pd

df = pd.read_csv("../../data/csv/original/device.csv", dtype={'user': str})
print(df)
df = df[['user', 'start_viewing_date', 'stop_viewing_date']]
df.dropna(inplace=True)

df['start_viewing_date'] = pd.to_datetime(df['start_viewing_date'])
df['stop_viewing_date'] = pd.to_datetime(df['stop_viewing_date'])
df['duration'] = (df['stop_viewing_date'] - df['start_viewing_date']).dt.total_seconds().astype(int)
df_minus = df[df['duration'] < 0]
df_plus = df[df['duration'] >= 0]

df_plus['category'] = 'device'
df_plus = df_plus.rename(columns={'start_viewing_date': 'date'})
df_plus = df_plus[['user', 'date', 'duration', 'category']]
df_plus['date'] = df_plus['date'].dt.strftime('%Y/%m/%d %H:%M:%S')

print(df)

df_plus.to_csv("../../data/csv/original/device_fix.csv", index=False)
df_minus.to_csv("../../data/csv/original/device_minus.csv", index=False)