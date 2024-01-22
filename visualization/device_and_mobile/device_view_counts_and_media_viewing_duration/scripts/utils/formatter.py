#formatter.py
import pandas as pd
from datetime import datetime
import glob
import os

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

# ユーザー毎の除外日リスト（ユーザー追加可能）
exclusion_dates = {
    '2387': ['2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
}

def process_file(file_path, output_file_name):
    df = pd.read_csv(file_path)
    df['user'] = df['user'].apply(lambda x: f'{x:04d}')
    df['start_viewing_date'] = pd.to_datetime(df['start_viewing_date']).dt.tz_localize(None)#dt.tz_localize(None): datetimeオブジェクトのタイムゾーン情報をNoneに設定
    filtered_df = pd.DataFrame()
    for user, (start_date, end_date) in date_ranges.items():
        exclusion_date_list = []
        start_date = pd.to_datetime(start_date).date() #start_date(ex): 2022-11-23
        end_date = pd.to_datetime(end_date).date()
        user_data = df[df['user'] == user]

        # exclusion_datesに含まれる日をuser_data(DF)から除外
        if user in exclusion_dates:
            exclusion_date_list = [pd.to_datetime(date).date() for date in exclusion_dates[user]] #exlusion_date_list: [datetime.date(2022, 11, 20), ...]
            user_data = user_data[~user_data['start_viewing_date'].dt.date.isin(exclusion_date_list)]

        # user_data(DF)からdate_rangeの日付以外の行を除外。 .dt.date: datetime.dateオブジェクトに変換。
        user_data = user_data[(user_data['start_viewing_date'].dt.date >= start_date) & (user_data['start_viewing_date'].dt.date <= end_date)]
        day_counter = 1
        dummy_data_list = []
        # 日付範囲を反復処理し、日付のデータが存在する場合は day_counterをインクリメント
        for date in pd.date_range(start=start_date, end=end_date):
            date_obj = date.to_pydatetime().date()
            if date_obj in exclusion_date_list: # date_objのkeyが除外日リストに含まれる場合スキップ
                continue
            if user_data['start_viewing_date'].dt.date.isin([date_obj]).any(): #.any():列(シリーズ)全体に適用
                user_data.loc[user_data['start_viewing_date'].dt.date == date_obj, 'days'] = day_counter # .loc[条件, 列名]: trueの時、列にアクションを行う
                day_counter += 1
            else: # 特定の日付にデータが存在しない場合に、dummy_data辞書にdummy_data_listに追加
                dummy_data = {
                    'user': user,
                    'start_viewing_date': pd.Timestamp(date_obj),
                    'days': day_counter
                }
                if 'device_id' in df.columns:
                    dummy_data['device_id'] = 9  # Dummy value
                if 'viewing_duration' in df.columns:
                    dummy_data['viewing_duration'] = 0
                if 'media' in df.columns:
                    dummy_data['media'] = float('nan')
                dummy_data_list.append(dummy_data)
                day_counter += 1 # データが存在しない日でもday_counterをインクリメントするが、出力しない

        if dummy_data_list:
            dummy_df = pd.DataFrame(dummy_data_list)
            user_data = pd.concat([user_data, dummy_df])
        filtered_df = pd.concat([filtered_df, user_data])

    filtered_df['days'] = filtered_df['days'].astype(int) # filtered_dfのdaysの値を整数へ変更(小数点の排除)
    filtered_df = filtered_df.sort_values(by=['user', 'start_viewing_date'])
    filtered_df.reset_index(drop=True, inplace=True) #drop=True: 古いindexをDFから削除。 inplace=True: indexのresetをfiltered_dfに直接適用

    output_file_path = os.path.join('./filtered_csv/', output_file_name)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    filtered_df.to_csv(output_file_path, index=False)

    for user in date_ranges.keys():
        user_data = filtered_df[filtered_df['user'] == user]
        max_days = user_data['days'].max()
        if max_days == 14:
            print(f'User {user}: Max days is 14')
        else:
            print(f'User {user}: Max days is not 14, it is {max_days}')
        if user in exclusion_dates:
            exclusion_date_list = [pd.to_datetime(date).date() for date in exclusion_dates[user]]
            user_data = user_data[~user_data['start_viewing_date'].dt.date.isin(exclusion_date_list)]

process_file('./csv/device.csv', 'filtered_device.csv')
print('filtered_device.csv completed.')
process_file('./csv/media.csv', 'filtered_media.csv')
print('filtered_media.csv completed.')