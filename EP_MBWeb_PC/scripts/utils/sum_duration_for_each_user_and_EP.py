import pandas as pd
from itertools import product
import os

input_folder = "../../data/csv/0sec_category0/"
output_folder = "../../data/csv/complete0/"
os.makedirs(output_folder, exist_ok=True)

user_list = ['0765', '0816', '1143', '2387', '2457', '3613', '3828', '4545', '4703', '5711', '5833', '6420', '7471', '8058', '9556']
period_list = ['EP1', 'EP2']

for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})
        print(df)

        df = df.groupby(['user', 'period', 'category'])['duration'].sum().reset_index()

        # Create all combinations of users, 24-hour categories, and periods
        all_combinations = pd.DataFrame(product(user_list, period_list), columns=['user', 'period'])

        # Merge the original dataframe with all combinations and fill missing values with 0
        df_full = pd.merge(all_combinations, df, on=['user', 'category', 'period'], how='left').fillna(0)
        df_full['duration'] = df_full['duration'].astype(int)

        df = df.sort_values(['period', 'user', 'category'])

        print(df)
        df.to_csv(output_file_path, index=False)
