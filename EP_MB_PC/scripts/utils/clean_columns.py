import pandas as pd
import os

input_folder = "../../data/csv/original/"
output_folder = "../../data/csv/clean/"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})
        df['user'] = df['user'].str.zfill(4)

        df = df[['user', 'date', 'duration']]
        df.dropna(inplace=True)

        df['category'] = filename

        print(df)
        print(df['category'].value_counts(dropna=False))

        df.to_csv(output_file_path, index=False)
