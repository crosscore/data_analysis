import pandas as pd

file_path = '../../data/csv/original/device_original_with_category.csv'
df = pd.read_csv(file_path)

# Calculate number of matches for 'category' and 'predict_category' columns
matches = (df['category'] == df['predict_category']).sum()
match_rate = matches / len(df) * 100

print(f"一致率: {match_rate:.2f}%")