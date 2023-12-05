#delete_1143_5711.py
import pandas as pd
from datetime import datetime
import os

output_path = './delete_1143_5711/APP_add_days_del_user.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

input_file = './APP_add_days.csv'

### input_fileのuser列から'1143'と'5711'の行を全て削除する ###
df = pd.read_csv(input_file)

# user列の書式を変換する
df['user'] = df['user'].astype(str).str.zfill(4)  # 4桁の文字列に変換

#dfから'user'の値が'1143'と'5711'であるデータを除外する
df = df[~df['user'].isin(['1143', '5711'])]
df.to_csv(output_path, index=False)

# userごとに最大のdays値をチェックする
max_days_per_user = df.groupby('user')['days'].max()
print(max_days_per_user)

# userのデータのユニーク数をチェックする
unique_users = df['user'].nunique()
print(f'\nunique_users: {unique_users}')