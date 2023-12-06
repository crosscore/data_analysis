import pandas as pd

df = pd.read_csv('../../data/csv/device_with_category.csv', dtype={'user': str})

#dfのnanの列を表示する
print(df.isnull().any())
print(df.isnull().sum())
print(df.describe())

#dfの'action'の種類別のcountを表示
print(df['action'].value_counts())