import pandas as pd
import os

input_file_folder = "../../data/csv/original/"
output_folder = "../../data/csv/add_counts/"
os.makedirs(output_folder, exist_ok=True)

# Define user_list and period_list
user_list = ['0765', '0816', '1143', '2387', '2457', '3613', '3828', '4545', '4703', '5711', '5833', '6420', '7471', '8058', '9556']
period_list = ['EP1', 'EP2']
weekdays_list = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

for file in os.listdir(input_file_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_file_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})

        # Create a DataFrame with all combinations of user and period
        all_combinations = pd.MultiIndex.from_product([user_list, period_list], names=['user', 'period']).to_frame(index=False)

        # Group and count unique values while keeping the 'category' column
        counts = df.groupby(['user', 'period', 'category', 'weekdays'])['unique'].nunique().reset_index(name='counts')

        # Create a DataFrame with all combinations of user, period, and category
        all_combinations = pd.MultiIndex.from_product([user_list, period_list, df['category'].unique()], names=['user', 'period', 'category']).to_frame(index=False)

        # Merge and fill missing values with 0, then convert counts to integers
        merged_df = all_combinations.merge(counts, on=['user', 'period', 'category'], how='left').fillna(0)
        merged_df['counts'] = merged_df['counts'].astype(int)

        # weekdays列をカテゴリカルデータに変換し、weekdays_listの順序に従ってソート
        merged_df['weekdays'] = pd.Categorical(merged_df['weekdays'], categories=weekdays_list, ordered=True)
        merged_df = merged_df.sort_values(['period', 'user', 'weekdays'])  # 'weekdays'をソート条件に追加

        merged_df.to_csv(output_file_path, index=False)
