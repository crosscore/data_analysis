import pandas as pd

def calculate_duration(start, stop):
    """
    Calculate the duration in seconds between two datetime objects.
    """
    return (stop - start).total_seconds()

df = pd.read_csv("../../csv/device/all/all_device.csv", dtype={'user': str})
df['start_viewing_date'] = pd.to_datetime(df['start_viewing_date'])
df['stop_viewing_date'] = pd.to_datetime(df['stop_viewing_date'])

df['duration'] = df.apply(lambda row: int(calculate_duration(row['start_viewing_date'], row['stop_viewing_date'])), axis=1)
#user,device_id,action,start_viewing_date,stop_viewing_date,article_url,article_title,duration
df = df[['user', 'device_id', 'action', 'start_viewing_date', 'stop_viewing_date', 'duration', 'article_url', 'article_title']]

df = df[df['duration'] >= 0]

df.to_csv("../../csv/device/all/device.csv", index=False)
