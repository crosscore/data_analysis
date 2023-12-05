import pandas as pd
from datetime import datetime
from datetime import timedelta

# date_ranges = {user: {'実験開始日', '実験終了日'}, ...}
date_ranges = {
    '0765': ('2022-11-23', '2022-12-06'),
    '0816': ('2022-11-22', '2022-12-05'),
    '1143': ('2022-11-26', '2022-12-09'),
    '2387': ('2022-11-18', '2022-12-05'),
    '2457': ('2022-11-22', '2022-12-05'),
    '3613': ('2022-11-19', '2022-12-02'),
    '3828': ('2022-11-18', '2022-12-01'),
    '4545': ('2022-11-15', '2022-11-28'),
    '4703': ('2022-11-27', '2022-12-10'),
    '5711': ('2022-11-28', '2022-12-11'),
    '5833': ('2022-11-28', '2022-12-11'),
    '6420': ('2022-11-25', '2022-12-08'),
    '7471': ('2022-11-23', '2022-12-06'),
    '8058': ('2022-11-26', '2022-12-09'),
    '9556': ('2022-11-24', '2022-12-07'),
}

# ユーザー毎の実験除外日リスト（ユーザー追加可能）
exclusion_dates = {
    '2387': ['2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
}

csv_files = ['APP.csv', 'MB.csv', 'PC.csv', 'TV.csv']
combined_df = pd.DataFrame()

for file in csv_files:
    media_name = file.split('.')[0]
    df = pd.read_csv(file, dtype={'user': str})
    df['user'] = df['user'].astype(str).str.zfill(4)
    df['media'] = media_name
    
    # start_viewing_dateのフォーマット変更と範囲内のデータを保持
    df['start_viewing_date'] = pd.to_datetime(df['start_viewing_date'], format='%Y/%m/%d %H:%M:%S')
    df.rename(columns={'start_viewing_date': 'date'}, inplace=True)
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    df = df[df['user'].apply(lambda x: x in date_ranges)]
    # start_viewing_dateをdateに更新
    df = df[df.apply(lambda x: date_ranges[x['user']][0] <= x['date'] <= date_ranges[x['user']][1], axis=1)]

    # 各ユーザーの最初の視聴日を記録
    user_first_day = {user: datetime.strptime(date, '%Y-%m-%d').date() for user, (date, _) in date_ranges.items()}

    def calculate_days(row):
        user = row['user']
        current_date = datetime.strptime(row['date'], '%Y-%m-%d').date()
        
        # 除外日リストが存在するユーザーはそのリストを使用
        if user in exclusion_dates:
            if str(current_date) in exclusion_dates[user]:
                return None  # 除外日はNoneを返す
            else:
                valid_days = [str(user_first_day[user] + pd.Timedelta(days=i)) 
                              for i in range((current_date - user_first_day[user]).days + 1)
                              if str(user_first_day[user] + pd.Timedelta(days=i)) not in exclusion_dates[user]]
                return len(valid_days)
        else:
            # 除外日リストがない場合は開始日からの差を使用
            return (current_date - user_first_day[user]).days + 1

    df['days'] = df.apply(calculate_days, axis=1)
    df.dropna(subset=['days'], inplace=True) # Noneでdaysが設定された行を削除
    df['days'] = df['days'].astype(int)
    combined_df = pd.concat([combined_df, df])

# Debug
print(combined_df.head())
for user, group in combined_df.groupby('user'):
    print(f"User {user} days:")
    print(group['days'].tolist())

user_max_days = combined_df.groupby('user')['days'].max()
print("\n各ユーザーの'days'カラムの最大値:")
print(user_max_days)

combined_df['date'] = pd.to_datetime(combined_df['date']).dt.strftime('%Y-%m-%d')
combined_df.to_csv('Combined_all_media.csv', index=False)
print("CSVファイルの結合が完了しました。")
