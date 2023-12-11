import pandas as pd
import glob

csv_files = glob.glob("../../csv/device/original/*.csv")
all_df = pd.DataFrame()
for f in csv_files:
    df = pd.read_csv(f, dtype={'user': str})
    all_df = pd.concat([all_df, df], ignore_index=True)
all_df = all_df[['user', 'device_id', 'action', 'start_viewing_date', 'stop_viewing_date', 'article_url', 'article_title']]
print(all_df)
all_df.to_csv("../../csv/device/original/all_device_only_concat.csv", index=False)

all_df = all_df.sort_values(['user', 'start_viewing_date'])

all_df['start_viewing_date'] = all_df['start_viewing_date'].astype(str)
all_df['stop_viewing_date'] = all_df['stop_viewing_date'].astype(str)
all_df['start_viewing_date'] = all_df['start_viewing_date'].str.replace(r'\+.*', '', regex=True)
all_df['stop_viewing_date'] = all_df['stop_viewing_date'].str.replace(r'\+.*', '', regex=True)

all_df = all_df.drop_duplicates(subset=['user', 'start_viewing_date', 'stop_viewing_date'])
print(f"Removed duplicates of 'start_viewing_date' and 'stop_viewing_datte'\n{all_df}")

all_df = all_df[all_df['action'] == 'view']
print(f"Extract only 'view':\n{all_df}")

# Set rows that cannot be converted to numbers to nan
all_df['start_viewing_date'] = pd.to_datetime(all_df['start_viewing_date'], errors='coerce')
all_df['stop_viewing_date'] = pd.to_datetime(all_df['stop_viewing_date'], errors='coerce')
# delete nan rows
all_df = all_df.dropna(subset=['start_viewing_date', 'stop_viewing_date'])
print(f"Delete rows where 'start_viewing_date' or 'stop_viewing_date' is nan\n{all_df}")

print(all_df.isna().sum())
all_df.to_csv("../../csv/device/original/all_device.csv", index=False)