import pandas as pd

df = pd.read_csv('../../data/csv/add_category/all_device_add_category.csv', dtype={'user': str})
print(df)

# Display the number of each category column in df (including nan values)
print(df['category'].value_counts(dropna=False))

# category列がnanの行のみをcsvとして出力
df[df['category'].isna()].to_csv('../../data/csv/add_category/category_nan_row.csv', index=False)