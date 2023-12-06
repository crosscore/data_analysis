#add_viewing_time.py
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('../../data/csv/device_with_category_add_days.csv', dtype={'user': str})

# stop_viewing_dateのフォーマットを変更して、viewing_time列を計算して追加する
def process_row(row):
    # start_viewing_dateをdatetimeオブジェクトに変換
    start = datetime.fromisoformat(row['start_viewing_date'])

    # stop_viewing_dateをdatetimeオブジェクトに変換し、9時間減算
    stop_str = row['stop_viewing_date']
    if '+' in stop_str:
        stop_str = stop_str.split('+')[0]
    stop = datetime.fromisoformat(stop_str) - timedelta(hours=9)

    # viewing_timeを計算
    viewing_time = int((stop - start).total_seconds())
    
    return stop.strftime("%Y-%m-%d %H:%M:%S"), viewing_time

# 新しいstop_viewing_dateとviewing_timeをdfに追加
df[['stop_viewing_date', 'viewing_time']] = df.apply(process_row, axis=1, result_type='expand')

df = df[['user', 'category', 'viewing_time', 'days']]

df.to_csv('../../data/csv/category_days_viewing_time.csv', index=False)
print(df)

