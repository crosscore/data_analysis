import pandas as pd

# CSVファイルを読み込む
df = pd.read_csv('TV.csv')

# 'User'列の値を4桁の文字列に変換
df['User'] = df['User'].apply(lambda x: f'{x:04d}')

# 結果を新しいCSVファイルに保存（または同じファイルに上書き）
df.to_csv('TV.csv', index=False)