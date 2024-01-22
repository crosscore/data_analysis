import pandas as pd
from datetime import datetime
import os

input_file_list = ['MB', 'PC', 'TV', 'APP']

# date_ranges: userのdateがvalueの日付以降の行はcsvから除外
date_ranges = {
    '0765': '2022-11-23',
    '0816': '2022-11-22',
    '1143': '2022-11-26',
    '2387': '2022-11-18',
    '2457': '2022-11-22',
    '3613': '2022-11-19',
    '3828': '2022-11-18',
    '4545': '2022-11-15',
    '4703': '2022-11-27',
    '5711': '2022-11-28',
    '5833': '2022-11-28',
    '6420': '2022-11-25',
    '7471': '2022-11-23',
    '8058': '2022-11-26',
    '9556': '2022-11-24'
}

def keep_row(row):
    user_str = row['user'].zfill(4)
    if user_str in date_ranges:
        cut_off_date = datetime.strptime(date_ranges[user_str], '%Y-%m-%d') #日付オブジェクトに変換 ex. 2022-11-22 00:00:00
        return row['date'] < cut_off_date
    return True

for input_file in input_file_list:
    df = pd.read_csv(f'{input_file}.csv', dtype={'user': str})
    df['date'] = pd.to_datetime(df['date'])

    filtered_df = df[df.apply(keep_row, axis=1)]
    filtered_df['user'] = filtered_df['user'].apply(lambda x: x.zfill(4))
    
    output_dir = '../filtered/csv_date_range/'
    output_file = f'{input_file}_date_range.csv'
    output_path = os.path.join(output_dir, output_file)
    os.makedirs(output_dir, exist_ok=True)
    filtered_df.to_csv(output_path, index=False)