import pandas as pd
import os

df = pd.read_csv("../../data/csv/original/device.csv", dtype={'user': str})
df['date'] = pd.to_datetime(df['date'])
df['category'] = 'device'

df = df[['user', 'date', 'duration', 'category']]
df['date'] = df['date'].dt.strftime('%Y/%m/%d %H:%M:%S')
print(df)

output_file = "../../data/csv/clean/device.csv"
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_csv(output_file, index=False)