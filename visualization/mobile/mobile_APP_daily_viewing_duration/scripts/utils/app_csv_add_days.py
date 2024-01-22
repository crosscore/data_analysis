#APP_filtered_date_range.csvにdays列を追加（days列の値を計算）

import pandas as pd
from datetime import datetime
import os

output_path = '../data/csv/filtered_date_range/add_days/APP_add_days.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

df = pd.read_csv('../data/csv/filtered_date_range/APP_filtered_date_range.csv', parse_dates=['date'], dtype={'user': str})
df['user'] = df['user'].astype(str).str.zfill(4)

# userごとにグループ化し、各userの最新の日付を取得する
earliest_date_per_user = df.groupby('user')['date'].min()

def calculate_days_column(group_data):
    group_data = group_data.sort_values('date')
    group_data['days'] = 0
    prev_date = None
    day_counter = 0
    for index, row in group_data.iterrows():
        current_date = row['date']
        if prev_date is None or current_date > prev_date:
            day_counter += 1
        group_data.at[index, 'days'] = day_counter
        prev_date = current_date
    return group_data

result_df = df.groupby('user').apply(calculate_days_column)
result_df = result_df.reset_index(drop=True)
max_days_per_user = result_df.groupby('user')['days'].max()
print(max_days_per_user)

result_df.to_csv(output_path, index=False)
