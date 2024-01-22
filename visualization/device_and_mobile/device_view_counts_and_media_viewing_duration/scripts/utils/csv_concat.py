import pandas as pd

df_app = pd.read_csv('APP_add_days.csv', dtype={'user': str})
df_media = pd.read_csv('Combined_all_media.csv', dtype={'user': str})

# データフレームを縦に結合する
df_combined = pd.concat([df_app, df_media], ignore_index=True)
# 'user'と'date'のカラムで降順にソートする
df_sorted = df_combined.sort_values(by=['user', 'date'], ascending=True)

df_sorted.to_csv('./concat_csv/APP_concat_media.csv', index=False)
