import pandas as pd
from datetime import datetime
import os

output_path = '../../data/csv/filtered/csv_date_range/MB_date_range.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

df = pd.read_csv('MB.csv', dtype={'user': str})

# Convert the 'date' column to datetime objects
df['date'] = pd.to_datetime(df['date'])

# Define the date ranges for each user
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

# Define the exclusion dates for user 2387
exclusion_dates = {
    '2387': ['2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
}

def keep_row(row):
    user_str = str(row['user']).zfill(4)
    date_range = date_ranges.get(user_str)

    # Convert exclusion dates to datetime.date for comparison
    exclusion_dates_list = exclusion_dates.get(user_str, [])
    exclusion_datetimes = [datetime.strptime(d, '%Y-%m-%d').date() for d in exclusion_dates_list]

    # Check if the date is in the exclusion list for user 2387
    if user_str == '2387' and row['date'].date() in exclusion_datetimes:
        return False

    if date_range:
        start_date = datetime.strptime(date_range[0], '%Y-%m-%d').date()
        end_date = datetime.strptime(date_range[1], '%Y-%m-%d').date()
        # Check if the date falls within the range
        return start_date <= row['date'].date() <= end_date
    return False

# Filter the DataFrame
filtered_df = df[df.apply(keep_row, axis=1)]

# Pad the 'user' column with zeros up to 4 digits
filtered_df.loc[:, 'user'] = filtered_df['user'].apply(lambda x: x.zfill(4))

filtered_df.to_csv(output_path, index=False)
