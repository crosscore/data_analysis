import pandas as pd
import os

input_folder = "../../data/csv/original/"
output_folder = "../../data/csv/complete/"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})
        print(df)

        df = df.groupby(['user', 'period'])['duration'].sum().reset_index()
        df = df.sort_values(['period', 'user'])
        df['category'] = filename

        print(df)
        df.to_csv(output_file_path, index=False)
