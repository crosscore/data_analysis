import pandas as pd

df = pd.read_csv("../../data/csv/original/MobileApp.csv", dtype={'user': str})
print(df)

df = df.groupby(['user', 'period', 'category'])['duration'].sum().reset_index()
df = df.sort_values(['period', 'user', 'category'])

print(df)
df.to_csv("../../data/csv/complete/MobileApp.csv", index=False)
