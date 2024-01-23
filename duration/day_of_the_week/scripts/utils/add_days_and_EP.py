import pandas as pd
from datetime import datetime, timedelta
import os

def create_combined_df(input_csv_path, output_dir):
    base_filename = os.path.basename(input_csv_path)
    output_filename = base_filename.replace('.csv', '.csv')
    exp1_start_date = pd.to_datetime('2022-10-22')
    exp1_end_date = pd.to_datetime('2022-11-04') + timedelta(days=1)
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
    exclusion_dates = pd.to_datetime(exclusion_date_user2387)

    def calculate_exp2_days(row):
        user = row['user']
        date = row['date']
        start_date = pd.Timestamp(exp2_ranges[user][0])
        if user == '2387':
            excluded_days_count = sum([1 for excl_date in exclusion_dates if start_date <= excl_date <= date])
            return (date - start_date).days + 1 - excluded_days_count
        else:
            return (date - start_date).days + 1

    def add_exp2_days(df):
        for date_str in exclusion_date_user2387:
            date = pd.to_datetime(date_str)
            df = df[~((df['user'] == '2387') & (df['date'] == date))]
        df['date'] = pd.to_datetime(df['date'])
        df.sort_values(by=['user', 'date'], ascending=[True, True], inplace=True)
        for user, (start, end) in exp2_ranges.items():
            end_date = pd.Timestamp(end) + timedelta(days=1)
            df = df[~((df['user'] == user) & ((df['date'] < pd.Timestamp(start)) | (df['date'] >= end_date)))]
        df['days'] = df.apply(calculate_exp2_days, axis=1)
        return df

    def parse_datetime(dt_str):
        try:
            return pd.to_datetime(dt_str, format='%Y/%m/%d %H:%M:%S')
        except ValueError:
            return pd.to_datetime(dt_str, format='%Y/%m/%d %H:%M')

    df = pd.read_csv(input_csv_path, dtype={'user': str})
    df['date'] = df['date'].apply(parse_datetime)
    df = df.sort_values(['user', 'date'])

    exp1_df = df[(df['date'] >= exp1_start_date) & (df['date'] < exp1_end_date)].copy()
    exp1_df['days'] = (exp1_df['date'] - exp1_start_date).dt.days + 1
    exp1_df['period'] = 'EP1'
    exp2_df = add_exp2_days(df.copy())
    exp2_df['period'] = 'EP2'
    combined_df = pd.concat([exp1_df, exp2_df])

    combined_df = combined_df.drop(columns=['program_name', 'app', 'TVエリア', '性年代', 'メディアターゲット区分', '仕事環境', '最終学歴', 'パッケージId', 'os', 'アプリ提供企業名'], errors='ignore')

    os.makedirs(output_dir, exist_ok=True)
    output_file_path = os.path.join(output_dir, output_filename)
    combined_df.to_csv(output_file_path, index=False)
    print(combined_df.groupby('user')['days'].max())
    print("Combined dataframe saved successfully.")

def process_all_files(input_folder, output_folder):
    for file in os.listdir(input_folder):
        if file.endswith(".csv"):
            input_csv_path = os.path.join(input_folder, file)
            create_combined_df(input_csv_path, output_folder)

input_folder = "../../data/csv/clean/"
output_folder = "../../data/csv/add_days"
os.makedirs(output_folder, exist_ok=True)
process_all_files(input_folder, output_folder)
