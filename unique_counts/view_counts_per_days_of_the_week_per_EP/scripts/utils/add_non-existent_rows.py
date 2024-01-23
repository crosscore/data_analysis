import pandas as pd
from itertools import product
import os

user_list = ['0765', '0816', '1143', '2387', '2457', '3613', '3828', '4545', '4703', '5711', '5833', '6420', '7471', '8058', '9556']
period_list = ['EP1', 'EP2']
weekdays_list = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

input_file_folder = "../../data/csv/add_counts/"
output_folder = "../../data/csv/complete/"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_file_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_file_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})
        
        # CSVデータからユニークなcategoryの値を取得する
        category_list = df['category'].unique().tolist()

        # 全ての組み合わせを生成する
        all_combinations = pd.DataFrame(list(product(user_list, period_list, category_list, weekdays_list)), columns=['user', 'period', 'category', 'weekdays'])

        # 元のDataFrameと全ての組み合わせをマージし、存在しない行はcountsの値を0として補完する
        df = pd.merge(all_combinations, df, on=['user', 'period', 'category', 'weekdays'], how='left').fillna(0)

        df = df.sort_values(['period', 'user']).reset_index(drop=True)
        df['counts'] = df['counts'].astype(int)

        df.to_csv(output_file_path, index=False)
        print(f"Processed {input_file_path} and saved to {output_file_path}")