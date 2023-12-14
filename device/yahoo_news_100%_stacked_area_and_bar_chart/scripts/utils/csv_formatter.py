import pandas as pd

df = pd.read_csv("../../data/csv/original/device_original_with_category.csv", dtype={'user': str})
print(df)

#user,action,device_id,start_viewing_date,stop_viewing_date,url,title,content,category
df = df[['user', 'action', 'device_id', 'start_viewing_date', 'stop_viewing_date', 'category']]
print(df)

df = df[df['category'] != '404_not_found']

df = df.dropna(subset=['category'])
print(df)
df.to_csv("../../data/csv/original/device_original_with_category_formatted.csv", index=False)