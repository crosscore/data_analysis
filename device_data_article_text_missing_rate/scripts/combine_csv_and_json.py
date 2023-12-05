#combine_csv_and_json.py
import pandas as pd
import json
import os

#all_user.csv, all_user.json を結合

df = pd.read_csv('../data/csv/all_user_csv/all_user.csv', dtype={'user': str})


with open('../data/json/all_user.json', encoding='utf-8') as f:
    json_data = json.load(f)
json_records = []
for item in json_data:
    record = {key: value['S'] for key, value in item['Item'].items() if key != 'thumbnail_url'}
    json_records.append(record)
json_df = pd.DataFrame(json_records)
print(json_df)

# 'article_url' と 'url' を基に inner join
merged_df = pd.merge(df, json_df, left_on='article_url', right_on='url', how='inner')

# 'url' 列を削除する
merged_df.drop('url', axis=1, inplace=True)
# 'user' 及び 'start_viewing_date'列で昇順ソート
merged_df.sort_values(by=['user', 'start_viewing_date'], ascending=True, inplace=True) #inplace=True:ソートを元のDFに直接適用

output_path = '../data/csv/combine_csv/all_user_plus_json.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged_df.to_csv(output_path, index=False)
