import pandas as pd
import os

input_file_folder = "../../data/csv/original/"
output_folder = "../../data/csv/complete/"
os.makedirs(output_folder, exist_ok=True)

user_list = ['0765', '0816', '1143', '2387', '2457', '3613', '3828', '4545', '4703', '5711', '5833', '6420', '7471', '8058', '9556']
period_list = ['EP1', 'EP2']
weekdays_list = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
twenty_four_list = list(range(24))

for file in os.listdir(input_file_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_file_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})

        #'date'列の時間(hour)の値を取得し、'24h'列を作成する
        df['24h'] = pd.to_datetime(df['date']).dt.hour

        # 'user', 'period', '24h'列でグループ化し、行数の合計値を元にcounts列を新たに作成する
        df = df.groupby(['user', 'period', '24h'])['unique'].nunique().reset_index(name='counts')

        # dfにおいて、twenty_four_listがuserとperiodの組み合わせごとに全て存在するようにする
        df = df.set_index(['user', 'period', '24h']).reindex(pd.MultiIndex.from_product([user_list, period_list, twenty_four_list], names=['user', 'period', '24h'])).reset_index()
        
        # NaNを0で埋める
        df['counts'] = df['counts'].fillna(0).astype(int)

        df = df.sort_values(['period', 'user', '24h']).reset_index(drop=True)

        # 24h列の名前を'hour'に変更する
        df = df.rename(columns={'24h': 'hour'})

        df.to_csv(output_file_path, index=False)