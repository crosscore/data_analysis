import pandas as pd

df = pd.read_csv('../../data/csv/add_days/device_add_days.csv', dtype={'user': str})

print(f"df['days'].min():{df['days'].min()}")
print(f"df['days'].max():{df['days'].max()}")

#dfの'user'毎のdaysの最大値を表示
print(df.groupby('user')['days'].max())

#dfのnanの列を表示する
print(df.isnull().any())
print(df.isnull().sum())
print(df.describe())

#dfの'action'の種類別のcountを表示
print(df['action'].value_counts())
