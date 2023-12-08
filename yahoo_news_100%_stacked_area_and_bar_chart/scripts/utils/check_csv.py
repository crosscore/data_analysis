import pandas as pd

#df = pd.read_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time.csv', dtype={'user': str})
df = pd.read_csv('../../data/csv/original/device_original_with_category.csv', dtype={'user': str})

# print(f"df['days'].min():{df['days'].min()}")
# print(f"df['days'].max():{df['days'].max()}")

##dfの'user'毎のdaysの最大値を表示
#print(df.groupby('user')['days'].max())

#dfのnanの列を表示する
print(df.isnull().sum())
print(df)