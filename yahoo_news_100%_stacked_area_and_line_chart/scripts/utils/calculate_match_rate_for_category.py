import pandas as pd

file_path = '../../data/csv/original/device_original_with_category.csv'
df = pd.read_csv(file_path)

# 'category' と 'predict_category' 列の一致数を計算
matches = (df['category'] == df['predict_category']).sum()
match_rate = matches / len(df) * 100

print(f"一致率: {match_rate:.2f}%")