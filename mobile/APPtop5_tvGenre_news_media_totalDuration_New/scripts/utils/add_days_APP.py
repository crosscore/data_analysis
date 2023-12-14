import pandas as pd
from datetime import datetime, timedelta

file = 'APP_date_range.csv'

# 除外する日付リスト
exclusion_date_user2387 = ['2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
exclusion_dates = pd.to_datetime(exclusion_date_user2387)

data = pd.read_csv(file, dtype={'user': str})
data.sort_values(by=['user', 'date'], ascending=[True, True], inplace=True)
data['date'] = pd.to_datetime(data['date'])

# 各ユーザーの最初の日付を取得
start_dates = data.groupby('user')['date'].min().to_dict()

def calculate_days(row):
    user = row['user']
    date = row['date']

    # ユーザー2387は特別に処理
    if user == '2387':
        # 最初の日は1とする
        if date == start_dates[user]:
            return 1
        # 除外日を越えていない日付は通常通りカウント
        elif date <= pd.Timestamp('2022-11-19'):
            return (date - start_dates[user]).days + 1
        # 除外日の翌日からは、除外された日数を考慮してカウント
        else:
            days_count = (date - start_dates[user]).days + 1  # 通常の日数
            # 除外日数を計算
            excluded_days_count = sum([1 for excl_date in exclusion_dates if start_dates[user] < excl_date < date])
            # 除外日数を差し引く
            return days_count - excluded_days_count
    else:
        # ユーザー2387以外は通常通り計算
        return (date - start_dates[user]).days + 1

# 'days' 列を計算して適用
data['days'] = data.apply(calculate_days, axis=1)

#不要な他のカラムを削除
#user,tv_erea,sex_age,media_target,environment,final_education,date,duration,os,package_id,app_categor,app_provider_name,app_name
data.drop(['tv_erea', 'sex_age', 'media_target', 'environment', 'final_education'], axis=1, inplace=True)

data.to_csv('../../complete/APP_1st.csv', index=False)

max_days_per_user = data.groupby('user')['days'].max()
print("各ユーザーの最大days値:")
print(max_days_per_user)