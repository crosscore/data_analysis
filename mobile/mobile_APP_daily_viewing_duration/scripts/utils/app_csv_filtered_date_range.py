#app_csv_filtered_date_range.py
#APP_filtered.csvの日付範囲をdate_rangesに限定
import pandas as pd
from datetime import datetime
import os

output_path = '../data/csv/filtered_date_range/APP_filtered_date_range.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

data = pd.read_csv('../data/csv//filtered/APP_filtered.csv', dtype={'user': str})

# date列の書式を変換する
data['date'] = data['date'].apply(lambda x: datetime.strptime(x.split(' ')[0], '%Y/%m/%d'))

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

# ユーザー毎の除外日リスト（ユーザー追加可能）
exclusion_dates = {
    '2387': ['2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
}

# 日付の書式を変換する
for user, dates in exclusion_dates.items():
    exclusion_dates[user] = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]

# userと日付の範囲に基づいてデータをフィルタリングする
filtered_data = pd.DataFrame()
for user, (start_date, end_date) in date_ranges.items():
    user_data = data[data['user'] == user]

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # date列をdateオブジェクトに変換
    user_data['date'] = user_data['date'].dt.date  
    
    # date列の範囲内のデータのみを抽出
    user_data = user_data[(user_data['date'] >= start_date) & (user_data['date'] <= end_date)]
    
    # 除外日のデータを除外
    if user in exclusion_dates:
        user_data = user_data[~user_data['date'].isin(exclusion_dates[user])]
    filtered_data = pd.concat([filtered_data, user_data])

filtered_data.to_csv(output_path, index=False)