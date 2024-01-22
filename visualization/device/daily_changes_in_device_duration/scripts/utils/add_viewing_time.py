#add_viewing_time.py
import pandas as pd
from datetime import datetime, timedelta
import os

df = pd.read_csv('../../data/csv/add_days/device_add_days.csv', dtype={'user': str})
print(df)

def process_row(row):
    start = datetime.fromisoformat(row['start_viewing_date'])
    stop = datetime.fromisoformat(row['stop_viewing_date'])
    viewing_time = int((stop - start).total_seconds())
    return viewing_time

df['viewing_time'] = df.apply(process_row, axis=1)
df = df[['user', 'viewing_time', 'days']]

output_file = '../../data/csv/add_viewing_time/device_add_days_viewing_time.csv'
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_csv(output_file, index=False)
print(df)