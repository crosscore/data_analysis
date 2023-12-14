import pandas as pd

df = pd.read_csv('../../data/csv/original/all_device_add_category_na.csv', dtype={'user': str})
print(df)

df_unique_url = df.drop_duplicates(subset=['url'])
print(df_unique_url)

df_unique_url.to_csv('../../data/csv/original/all_device_add_category_na_unique_url.csv', index=False)