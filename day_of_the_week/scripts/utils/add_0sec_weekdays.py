import pandas as pd
import os
from itertools import product

input_file_folder = "../../data/csv/outlier_removed/"
output_folder = "../../data/csv/add_0sec_weekdays/"
os.makedirs(output_folder, exist_ok=True)

weekdays_list = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
user_list = ['0765', '0816', '1143', '2387', '2457', '3613', '3828', '4545', '4703', '5711', '5833', '6420', '7471', '8058', '9556']
period_list = ['EP1', 'EP2']

for file in os.listdir(input_file_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_file_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})

        # columnsに指定した列の値の全ての組み合わせを取得し、データフレームに変換
        all_combinations = pd.DataFrame(list(product(user_list, period_list, weekdays_list)), columns=['user', 'period', 'weekdays'])

        # 各ユーザーの共通のカテゴリを取得
        common_categories = df.groupby(['user', 'period'])['category'].agg(lambda x: pd.Series.mode(x)[0] if not x.empty else None).reset_index()
        print(common_categories)

        # all_combinationsとdfの結合
        df_complete = pd.merge(all_combinations, df, on=['user', 'period', 'weekdays'], how='left')

        # カテゴリを追加
        df_complete = pd.merge(df_complete, common_categories, on=['user', 'period'], how='left', suffixes=('', '_y'))
        df_complete['category'] = df_complete['category'].fillna(filename) # If there is no category, use the filename as the category
        df_complete.drop('category_y', axis=1, inplace=True)

        df_complete['duration'] = df_complete['duration'].fillna(0).astype(int)

        df_complete.sort_values(by=['period', 'user'], inplace=True)

        df_complete.to_csv(output_file_path, index=False)

        # validation
        # expected_combinations = len(user_list) * len(period_list) * len(weekdays_list)
        # actual_combinations = df_complete.groupby(['user', 'period'])['weekdays'].nunique().sum()

        # if expected_combinations == actual_combinations:
        #     print(f"{filename}: 全ての組み合わせが含まれています。")
        # else:
        #     missing_combinations = expected_combinations - actual_combinations
        #     print(f"{filename}: {missing_combinations} 個の組み合わせが不足しています。")

        #print(df_complete.groupby(['user', 'period'])['weekdays'].nunique())



