import pandas as pd
import os

input_file_path = "../../data/csv/original/APP.csv"
base = os.path.basename(input_file_path)
filename, _ = os.path.splitext(base)
output_file_path = f'../../data/csv/original/{filename}_fix.csv'

df = pd.read_csv(input_file_path, dtype={'user': str})
df['user'] = df['user'].str.zfill(4)

df = df[['user', 'date', 'duration', 'category']]
df.dropna(inplace=True)

print(df)
print(df['category'].value_counts(dropna=False))

df.to_csv(output_file_path, index=False)