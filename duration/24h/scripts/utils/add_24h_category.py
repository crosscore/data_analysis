import pandas as pd
from itertools import product
import os

user_list = ['0765', '0816', '1143', '2387', '2457', '3613', '3828', '4545', '4703', '5711', '5833', '6420', '7471', '8058', '9556']
period_list = ['EP1', 'EP2']
h24_list = [f'{hour:02d}' for hour in range(24)]

input_file_folder = "../../data/csv/outlier_removed1.5/"
output_folder = "../../data/csv/complete1.5/"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_file_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_file_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})
        df['category'] = pd.to_datetime(df['date']).dt.strftime('%H')
        df = df.groupby(['user', 'category', 'period'])['duration'].sum().reset_index()

        # Create all combinations of users, 24-hour categories, and periods
        all_combinations = pd.DataFrame(product(user_list, h24_list, period_list), columns=['user', 'category', 'period'])

        # Merge the original dataframe with all combinations and fill missing values with 0
        df_full = pd.merge(all_combinations, df, on=['user', 'category', 'period'], how='left').fillna(0)
        df_full['duration'] = df_full['duration'].astype(int)

        df_full = df_full.sort_values(['period', 'user', 'category'])
        print(df_full)

        df_full.to_csv(output_file_path, index=False)

