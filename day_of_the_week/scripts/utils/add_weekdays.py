import pandas as pd
import os
from datetime import datetime

def convert_to_datetime(date_str):
    """
    Convert date string to datetime object.
    Handles two formats: 'YYYY-MM-DD HH:MM:SS' and 'YYYY/MM/DD HH:MM:SS'
    """
    for fmt in ('%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S'):
        try:
            print(datetime.strptime(date_str, fmt))
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError(f'No valid date format found for {date_str}')

input_file_folder = "../../data/csv/add_days/"
output_folder = "../../data/csv/add_weekdays/"
os.makedirs(output_folder, exist_ok=True)
for file in os.listdir(input_file_folder):
    if file.endswith(".csv"):
        input_file_path = os.path.join(input_file_folder, file)
        filename, _ = os.path.splitext(file)
        output_file_path = os.path.join(output_folder, f'{filename}.csv')

        df = pd.read_csv(input_file_path, dtype={'user': str})
        df['user'] = df['user'].str.zfill(4)

        # Convert date column to datetime and extract weekday
        df['date'] = df['date'].apply(convert_to_datetime)
        df['weekdays'] = df['date'].apply(lambda x: x.strftime('%a').upper())

        df.to_csv(output_file_path, index=False)
        print(f"Processed {input_file_path} and saved to {output_file_path}")
