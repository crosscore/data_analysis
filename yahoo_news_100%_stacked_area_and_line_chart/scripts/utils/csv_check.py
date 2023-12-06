import pandas as pd

df = pd.read_csv('../../data/csv/category_days.csv', dtype={'user': str})

print(df['days'].min())
print(df['days'].max())