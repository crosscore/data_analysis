#add_duration.py
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('../../data/csv/1st_half_and_2nd_half/device_1st_half_and_2nd_half.csv', dtype={'user': str})
print(df)

def process_row(row):
    start = datetime.fromisoformat(row['start_viewing_date'])
    stop = datetime.fromisoformat(row['stop_viewing_date'])
    duration = int((stop - start).total_seconds())
    return duration

df['duration'] = df.apply(process_row, axis=1)
df = df[['user', 'category', 'duration', 'days']]

df = df[df['duration'] >= 0]

df.to_csv('../../data/csv/add_duration/device_add_duration.csv', index=False)
print(df)