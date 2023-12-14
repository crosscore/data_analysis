import pandas as pd
import glob
import os

#15人分のCSVファイルを1つに結合する

filepaths = glob.glob('../data/csv/original_csv/[0-9][0-9][0-9][0-9].csv')
all_data = [pd.read_csv(filepath) for filepath in filepaths]
merged_data = pd.concat(all_data, ignore_index=True)
merged_data['user'] = merged_data['user'].apply(lambda x: str(x).zfill(4))
print(merged_data)

cols = ['user'] + [col for col in merged_data if col != 'user']
merged_data = merged_data[cols]

output_path = '../data/csv/all_user_csv/all_user.csv'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged_data.to_csv(output_path, index=False)