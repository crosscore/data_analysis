import pandas as pd
import os

input_folder = "../../data/csv/add_0sec_weekdays0/"
output_folder = "../../data/csv/complete0/"
os.makedirs(output_folder, exist_ok=True)

weekdays_list = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})
        print(df)

        df = df.groupby(['user', 'period', 'weekdays', 'category'])['duration'].sum().reset_index()
        # weekdays列をカテゴリカルデータに変換し、weekdays_listの順序に従ってソート
        df['weekdays'] = pd.Categorical(df['weekdays'], categories=weekdays_list, ordered=True)
        df = df.sort_values(['period', 'user', 'weekdays'])  # 'weekdays'をソート条件に追加

        print(df)
        df.to_csv(output_file_path, index=False)
