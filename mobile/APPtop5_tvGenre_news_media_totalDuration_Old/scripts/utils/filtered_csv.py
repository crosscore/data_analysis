import pandas as pd

df = pd.read_csv('../../data/csv/APP_and_media_original.csv', dtype={'user': str})

# 'app_category'が'ツール類'または'ニュース'、または'media'列に値がある行を保持
#df = df[(df['app_category'].isin(['ツール類', 'ニュース'])) | df['media'].notna()]

# # 'days' 列を取得し一時的に保存
# days = df['days']

# 'days' 列を削除
# df.drop(['date'], axis=1, inplace=True)

#不要な他のカラムを削除
df.drop(['os', 'package_id', 'app_provider_name', 'date'], axis=1, inplace=True)

# # 'days' 列をDataFrameの最後に追加
# df['days'] = days

df.to_csv('APP_and_media.csv', index=False)