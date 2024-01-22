import pandas as pd

def filter_dates(df):
    exp1_range = ['2022-10-22', '2022-11-04']
    exp2_ranges = {
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

    df['date'] = pd.to_datetime(df['date'])
    exclusion_dates_2387 = pd.to_datetime(exclusion_date_user2387)

    filtered_dfs = [] 
    df_exp1 = df[df['date'].between(*pd.to_datetime(exp1_range))]
    filtered_dfs.append(df_exp1)

    for user, (start_date, end_date) in exp2_ranges.items():
        df_user = df[df['user'] == user]
        if user == '2387':
            df_user = df_user[~df_user['date'].isin(exclusion_dates_2387)]
        df_user = df_user[df_user['date'].between(pd.to_datetime(start_date), pd.to_datetime(end_date))]
        filtered_dfs.append(df_user)
    filtered_df = pd.concat(filtered_dfs)
    filtered_df = filtered_df.sort_values(by=['user', 'date'])
    return filtered_df

df = pd.read_csv("../../data/csv/original/MobileApp.csv", dtype={'user': str})
print(df)
print(df['app_category'].value_counts(dropna=False))

df = filter_dates(df)
print(df)
print(df['app_category'].value_counts(dropna=False))

df.dropna(subset=['app_category'], inplace=True)
print(df)
print(df['app_category'].value_counts(dropna=False))

df.to_csv("../../data/csv/date_range/MobileApp_date_range_dropna.csv", index=False)