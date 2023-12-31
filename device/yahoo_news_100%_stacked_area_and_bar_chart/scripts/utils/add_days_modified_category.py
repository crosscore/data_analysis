#add_days.py
import pandas as pd
from datetime import datetime, timedelta

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

df = pd.read_csv("../../data/csv/original/device_original_with_category_plus_modified.csv", dtype={'user': str})
not_found_count = df['modified_category'].value_counts().get('404_not_found', 0)
print("categoryが404_not_foundの行数:", not_found_count)
#df = df[df['modified_category'] != '404_not_found']

#Output the number of rows where the value of df['action'] is 'open'
open_count = df['action'].value_counts().get('open', 0)
print("open lines count:", open_count)

#Output the number of rows where the value of df['modified_category'] is nan
nan_count = df['modified_category'].isna().sum()
print("Number of lines where modified_category is nan:", nan_count)

df = df[df['action'] == 'view']
df = df.dropna(subset=['start_viewing_date', 'stop_viewing_date', 'modified_category'])
print(df['modified_category'].value_counts(dropna=False))

exclusion_date_user2387 = ['2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
exclusion_dates = pd.to_datetime(exclusion_date_user2387)

# Exclude date data included in exclusion_date_user2387 in user '2387' line
for date in exclusion_date_user2387:
    df = df[~((df['user'] == '2387') & df['start_viewing_date'].str.contains(date))]

df['start_viewing_date'] = pd.to_datetime(df['start_viewing_date'])
df['stop_viewing_date'] = pd.to_datetime(df['stop_viewing_date'])
df.sort_values(by=['user', 'start_viewing_date'], ascending=[True, True], inplace=True)

# delete data outside date_ranges
for user, (start, end) in date_ranges.items():
    end_date = pd.Timestamp(end) + timedelta(days=1)
    df = df[~((df['user'] == user) & ((df['start_viewing_date'] < pd.Timestamp(start)) | (df['start_viewing_date'] >= end_date)))]

def calculate_days(row, date_ranges):
    user = row['user']
    date = row['start_viewing_date']
    start_date = pd.Timestamp(date_ranges[user][0])
    end_date = pd.Timestamp(date_ranges[user][1])
    if user == '2387':
        excluded_days_count = sum([1 for excl_date in exclusion_dates if start_date <= excl_date <= date])
        days_count = (date - start_date).days + 1 - excluded_days_count
    else:
        days_count = (date - start_date).days + 1
    return days_count

df['days'] = df.apply(lambda row: calculate_days(row, date_ranges), axis=1)

#url,user,action,device_id,article_title,start_viewing_date,stop_viewing_date,eliminate_date,base_date,published_date,body,title,category,days
#user,url,action,device_id,category,days
df = df[['user', 'action', 'device_id', 'modified_category', 'start_viewing_date', 'stop_viewing_date','days']]

print(df.head())
print(df.describe())
df.to_csv("../../data/csv/add_days/device_add_days_modified_category.csv", index=False)

print(f'df["days"].min(): {df["days"].min()}')
print(f'df["days"].max(): {df["days"].max()}')

print(df.groupby('user')['days'].max())