import pandas as pd
import os

input_file_folder = "../../data/csv/add_days/"
output_folder = "../../data/csv/complete/"
os.makedirs(output_folder, exist_ok=True)

# Define user_list and period_list
user_list = ['0765', '0816', '1143', '2387', '2457', '3613', '3828', '4545', '4703', '5711', '5833', '6420', '7471', '8058', '9556']
period_list = ['EP1', 'EP2']

for file in os.listdir(input_file_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_file_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})

        # Create a DataFrame with all combinations of user and period
        all_combinations = pd.MultiIndex.from_product([user_list, period_list], names=['user', 'period']).to_frame(index=False)

        # Group and count unique values while keeping the 'category' column
        counts = df.groupby(['user', 'period', 'category'])['unique'].nunique().reset_index(name='counts')

        # Create a DataFrame with all combinations of user, period, and category
        all_combinations = pd.MultiIndex.from_product([user_list, period_list, df['category'].unique()], names=['user', 'period', 'category']).to_frame(index=False)

        # Merge and fill missing values with 0, then convert counts to integers
        merged_df = all_combinations.merge(counts, on=['user', 'period', 'category'], how='left').fillna(0)
        merged_df['counts'] = merged_df['counts'].astype(int)

        merged_df.to_csv(output_file_path, index=False)
