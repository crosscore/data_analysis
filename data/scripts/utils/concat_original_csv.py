import pandas as pd
import glob

csv_files = glob.glob("../../csv/device/original/*.csv")
all_df = pd.DataFrame()
for f in csv_files:
    df = pd.read_csv(f, dtype={'user': str})
    all_df = pd.concat([all_df, df], ignore_index=True)

all_df = all_df[['user', 'device_id', 'action', 'start_viewing_date', 'stop_viewing_date', 'article_url', 'article_title']]
# 'user'と'start_viewing_date'でソート
print(all_df)
all_df = all_df.sort_values(['user', 'start_viewing_date'])
# 'start_viewing_date'と'stop_viewing_date'を全てstr型に変換
all_df['start_viewing_date'] = all_df['start_viewing_date'].astype(str)
all_df['stop_viewing_date'] = all_df['stop_viewing_date'].astype(str)
# 'start_viewing_date'と'stop_viewing_date'の'+'以降の全ての文字列を削除
all_df['start_viewing_date'] = all_df['start_viewing_date'].str.replace(r'\+.*', '', regex=True)
all_df['stop_viewing_date'] = all_df['stop_viewing_date'].str.replace(r'\+.*', '', regex=True)
# 'start_viewing_date'列をdatetime型に変換
all_df['start_viewing_date'] = pd.to_datetime(all_df['start_viewing_date'], errors='coerce')
all_df['stop_viewing_date'] = pd.to_datetime(all_df['stop_viewing_date'], errors='coerce')
# 'start_viewing_date'と'stop_viewing_date'の値がnanの行を削除
all_df = all_df.dropna(subset=['start_viewing_date', 'stop_viewing_date'])
# 'action'が'view'以外の行を削除
all_df = all_df[all_df['action'] == 'view']
print(all_df)
# 'start_viewing_date'と'stop_viewing_date'の値が連続して同じ行は1行のみを残して削除
all_df = all_df.drop_duplicates(subset=['user', 'start_viewing_date', 'stop_viewing_date'])
print(all_df)
# nanの行の数を出力
print(all_df.isna().sum())
all_df.to_csv("../../csv/device/original/all_device.csv", index=False)