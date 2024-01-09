import pandas as pd

df = pd.read_csv("../../data/csv/original/TV.csv", dtype={'user': str})
print(df)

df = df.groupby(['user', 'period'])['duration'].sum().reset_index()

df = df.sort_values(['period', 'user'])
df['category'] = 'TV'

print(df)
df.to_csv("../../data/csv/complete/TV.csv", index=False)