import pandas as pd
import glob

# ファイルパスを取得
file_names = glob.glob('./before/[0-9][0-9][0-9][0-9].csv')

# 各ファイルを読み込み、action列の値が'view'であり、start_viewing_date列に値がある行だけを保持し、リストに格納
dataframes = []
for file in file_names:
  df = pd.read_csv(file, dtype={'user': str}) 
  df = df.loc[(df['action'] == 'view') & (df['start_viewing_date'].notnull())]
  dataframes.append(df)

# すべてのデータフレームを結合  
concatenated_df = pd.concat(dataframes, ignore_index=True)

# 必要な列だけを取り出す
filtered_df = concatenated_df[['user', 'device_id', 'start_viewing_date']]

# 結果を新しいCSVファイルに保存
filtered_df.to_csv('./device.csv', index=False)