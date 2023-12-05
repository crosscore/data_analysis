import pandas as pd
from datetime import datetime

device_df = pd.read_csv('../data/csv/device.csv', parse_dates=['start_viewing_date'])
media_df = pd.read_csv('media.csv', parse_dates=['start_viewing_date'])

# 日付範囲の定義
date_ranges = {
    '4545': ('2022-11-15', '2022-11-28'),
    '2387': ('2022-11-18', '2022-12-05'),
    '3828': ('2022-11-18', '2022-12-01'),
    '3613': ('2022-11-19', '2022-12-02'),
    '2457': ('2022-11-22', '2022-12-05'),
    '0816': ('2022-11-22', '2022-12-05'),
    '0765': ('2022-11-23', '2022-12-06'),
    '7471': ('2022-11-23', '2022-12-06'),
    '9556': ('2022-11-24', '2022-12-07'),
    '6420': ('2022-11-25', '2022-12-08'),
    '1143': ('2022-11-26', '2022-12-09'),
    '8058': ('2022-11-26', '2022-12-09'),
    '4703': ('2022-11-27', '2022-12-10'),
    '5833': ('2022-11-28', '2022-12-11'),
    '5711': ('2022-11-28', '2022-12-11'),
}

def calculate_days(df):
    for user, (start_date, end_date) in date_ranges.items():
        # user列を文字列に変換してから比較
        user_df = df[df['user'].astype(str) == user]
        user_df['date'] = user_df['start_viewing_date'].dt.date  # 日付の部分だけを抽出
        # start_dateとend_dateをdatetime.dateオブジェクトに変換してから比較
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        user_df = user_df[(user_df['date'] >= start_date) & (user_df['date'] <= end_date)]  # 日付範囲でフィルタリング
        print(user_df)
        if not user_df.empty:
            first_viewing_date = user_df['date'].min()
            user_df['days'] = (user_df['date'] - first_viewing_date).dt.days + 1
            df.loc[user_df.index, 'days'] = user_df['days']  # 元のデータフレームにdays列を更新

# days列を計算
calculate_days(device_df)
calculate_days(media_df)

device_df.to_csv('device_add_days.csv', index=False)
media_df.to_csv('media_add_days.csv', index=False)

