import pandas as pd
import os

input_file_path = "../../data/csv/split_EP2/MobileApp.csv"
base = os.path.basename(input_file_path)
filename, _ = os.path.splitext(base)
output_file_path = f'../../data/csv/0sec_category/{filename}.csv'

df = pd.read_csv(input_file_path, dtype={'user': str})

unique_categories = df['category'].unique()
final_df = pd.DataFrame()
for (user, period), group in df.groupby(['user', 'period']):
    missing_categories = set(unique_categories) - set(group['category'])
    missing_rows = pd.DataFrame({'user': user, 'period': period, 'category': list(missing_categories), 'duration': 0})
    final_df = pd.concat([final_df, group, missing_rows], ignore_index=True)

final_df = final_df.sort_values(['period', 'user', 'category']).reset_index(drop=True)

print(final_df)
final_df.to_csv(output_file_path, index=False)
