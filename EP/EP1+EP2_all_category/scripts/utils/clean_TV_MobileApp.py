import pandas as pd

df = pd.read_csv("../../data/csv/original/TV.csv", dtype={'user': str})
print(df)
df = df[['user', 'date', 'duration', 'category']]

df.dropna(inplace=True)

print(df)
print(df['category'].value_counts(dropna=False))

df.to_csv("../../data/csv/original/TV_fix.csv", index=False)