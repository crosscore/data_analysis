import pandas as pd
import os

input_file_path = "../../data/csv/original/MobileApp.csv"
base = os.path.basename(input_file_path)
filename, _ = os.path.splitext(base)
output_file_path = f'../../data/csv/split_EP2/{filename}.csv'

df = pd.read_csv(input_file_path, dtype={'user': str})
print(df)

# dfの'period'列の値が'EP2'の行のみを抽出
df = df[df['period'] == 'EP2']

df.loc[df['days'] <= 7, 'period'] = 'EP1'
df = df.sort_values(['period', 'user', 'date'])

print(df)
df.to_csv(output_file_path, index=False)