import pandas as pd

df = pd.read_csv('../../data/csv/device_with_category_add_days.csv', dtype={'user': str})

print(df['days'].min())
print(df['days'].max())

#dfのnanの列を表示する
print(df.isnull().any())
print(df.isnull().sum())
print(df.describe())

#dfの'action'の種類別のcountを表示
print(df['action'].value_counts())
