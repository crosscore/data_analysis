import pandas as pd
import os

input_file_folder = "../../data/csv/original/"
output_folder = "../../data/csv/cleaned/"
os.makedirs(output_folder, exist_ok=True)

for file in os.listdir(input_file_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_file_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})
        df['user'] = df['user'].str.zfill(4)

        df = df[['user', 'date', 'unique']]
        df.dropna(inplace=True)

        # Add 'category' column to df and set value to filename
        df['category'] = filename

        print(df)
        print(df['unique'].value_counts(dropna=False))
        
        # Convert 'date' column to datetime and format it
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y/%m/%d %H:%M:%S')

        df.to_csv(output_file_path, index=False)