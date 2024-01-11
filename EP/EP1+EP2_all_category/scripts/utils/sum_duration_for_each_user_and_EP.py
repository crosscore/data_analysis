import pandas as pd
import os

input_file_path = "../../data/csv//APP.csv"
base = os.path.basename(input_file_path)
filename, _ = os.path.splitext(base)
output_file_path = f'../../data/csv/complete/{filename}.csv'

df = pd.read_csv("../../data/csv/outlier_removed/TV_EP_outlier_removed.csv", dtype={'user': str})
print(df)

df = df.groupby(['user', 'period', 'category'])['duration'].sum().reset_index()
df = df.sort_values(['period', 'user', 'category'])

print(df)
df.to_csv(output_file_path, index=False)
