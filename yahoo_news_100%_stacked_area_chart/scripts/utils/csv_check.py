import pandas as pd

df = pd.read_csv('../../data/csv/category_days.csv', dtype={'user': str})
#dfのdays列の最小値と最大値を出力

print(df['days'].min())

print(df['days'].max())