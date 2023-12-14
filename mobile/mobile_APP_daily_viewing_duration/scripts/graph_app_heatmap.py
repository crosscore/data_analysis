import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import os

output_path = './img/graph_app_heatmap/Img_graph_app_heatmap.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
data = pd.read_csv('./APP_add_days_del_user.csv', dtype={'user': str})

# user, app, daysの列だけを取得
data = data[['user', 'app_name', 'days']]

# 各ユーザーと日付ごとに異なるアプリの数を集計
app_counts_per_user_per_day = data.groupby(['user', 'days']).nunique()['app_name']

# 結果をデータフレームに変換
heatmap_data = app_counts_per_user_per_day.unstack(fill_value=0)

# カラーマップの選択と範囲の調整
#colors = plt.cm.plasma(np.linspace(0, 20, len(heatmap_data.columns)))  # グラデーションカラーを設定

# ヒートマップを作成
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='viridis') # ex. cmap='viridis'
plt.title('Number of unique apps used per user per day')
plt.ylabel('User')
plt.xlabel('Day')
plt.tick_params(axis='y', rotation=0)
plt.savefig(output_path)
plt.close()
