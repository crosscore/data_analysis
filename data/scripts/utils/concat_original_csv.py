import pandas as pd
import glob

csv_files = glob.glob("../../csv/device/original/*.csv")
print(f"Found {len(csv_files)} CSV files.")

# Initialize a list to store dataframes
dfs = []

for f in csv_files:
    df = pd.read_csv(f, dtype={'user': str})
    dfs.append(df)  # Append each dataframe to the list
    print(f"Processed {f}, current DataFrame size: {len(df)}")  # Output the size of each processed dataframe

# Concatenate all dataframes at once
all_df = pd.concat(dfs, ignore_index=True)

# Select required columns
all_df = all_df[['user', 'device_id', 'action', 'start_viewing_date', 'stop_viewing_date', 'article_url', 'article_title']]

# Sort by user and start viewing date
all_df = all_df.sort_values(['user', 'start_viewing_date'])
print(f"Concat all user's csvs:\n{all_df}")

all_df['start_viewing_date'] = all_df['start_viewing_date'].astype(str)
all_df['stop_viewing_date'] = all_df['stop_viewing_date'].astype(str)
all_df['start_viewing_date'] = all_df['start_viewing_date'].str.replace(r'\+.*', '', regex=True)
all_df['stop_viewing_date'] = all_df['stop_viewing_date'].str.replace(r'\+.*', '', regex=True)

all_df = all_df[all_df['action'] == 'view']
print(f"Extract only 'view':\n{all_df}")

#all_df = all_df.drop_duplicates(subset=['user', 'start_viewing_date', 'stop_viewing_date'])

# Set rows that cannot be converted to numbers to nan
all_df['start_viewing_date'] = pd.to_datetime(all_df['start_viewing_date'], errors='coerce')
all_df['stop_viewing_date'] = pd.to_datetime(all_df['stop_viewing_date'], errors='coerce')

nan_rows = all_df[all_df.isna().any(axis=1)]

# delete nan rows
all_df = all_df.dropna(subset=['start_viewing_date', 'stop_viewing_date'])
print(f"Delete rows where 'start_viewing_date' or 'stop_viewing_date' is nan\n{all_df}")

nan_rows.to_csv("../../csv/device/all/nan_device.csv", index=False)

print(f"all_df.isna().sum()\n{all_df.isna().sum()}")
all_df.to_csv("../../csv/device/all/all_device.csv", index=False)