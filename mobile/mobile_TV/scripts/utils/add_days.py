#add_days.py
import pandas as pd
from datetime import datetime, timedelta
import os

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

exclusion_date_user2387 = ['2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
exclusion_dates = pd.to_datetime(exclusion_date_user2387)

# Function to add 'days' column
def add_days_to_df(df):
    # Exclude certain dates for user '2387'
    for date in exclusion_date_user2387:
        df = df[~((df['user'] == '2387') & df['date'].str.contains(date))]

    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['user', 'date'], ascending=[True, True], inplace=True)

    # Delete data outside date_ranges
    for user, (start, end) in date_ranges.items():
        end_date = pd.Timestamp(end) + timedelta(days=1)
        df = df[~((df['user'] == user) & ((df['date'] < pd.Timestamp(start)) | (df['date'] >= end_date)))]

    # Function to calculate days
    def calculate_days(row):
        user = row['user']
        date = row['date']
        start_date = pd.Timestamp(date_ranges[user][0])
        if user == '2387':
            excluded_days_count = sum([1 for excl_date in exclusion_dates if start_date <= excl_date <= date])
            return (date - start_date).days + 1 - excluded_days_count
        else:
            return (date - start_date).days + 1

    df['days'] = df.apply(calculate_days, axis=1)
    return df

# Read the data
df = pd.read_csv("../../data/csv/original/TV_before_add_duration_fix_user.csv", dtype={'user': str})

# Apply the function to both dataframes
df = add_days_to_df(df)

output_dir = '../../data/csv/add_days/'
os.makedirs(os.path.dirname(output_dir), exist_ok=True)

# Save the modified dataframes
df.to_csv(f"{output_dir}TV_add_days.csv", index=False)

# Print results
print(df.groupby('user')['days'].max())
