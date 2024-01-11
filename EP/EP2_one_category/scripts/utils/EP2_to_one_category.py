import pandas as pd
import os

input_file_path = "../../data/csv/original/TV.csv"
base = os.path.basename(input_file_path)
filename, _ = os.path.splitext(base)
output_file_path = f'../../data/csv/complete/{filename}.csv'

df = pd.read_csv(input_file_path, dtype={'user': str})
print(df)

df['category'] = filename
df = df.groupby(['user', 'period', 'category'])['duration'].sum().reset_index()
df = df.sort_values(by=['period','user'])

print(df)
df.to_csv(output_file_path, index=False)