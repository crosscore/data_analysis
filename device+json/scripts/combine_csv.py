import pandas as pd
import numpy as np

device_df = pd.read_csv("../data/csv/original/all_device_5409.csv", dtype={'user': str})
json_df = pd.read_csv("../data/csv/original/json_original.csv", dtype={'user': str})
print(device_df)
print(json_df)

print(json_df.isnull().sum())

json_df = json_df.dropna(subset=['body'])
print(json_df)

print(json_df.isnull().sum())