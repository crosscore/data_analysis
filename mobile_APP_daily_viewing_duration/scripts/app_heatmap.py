#app_heatmap.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib

output_path = './Img_app_heatmap.png'
data = pd.read_csv('./APP_add_days.csv', dtype={'user': str})

# user, app, daysの列だけを取得
data = data[['user', 'app_name', 'days']]

# 各ユーザーと日付ごとに異なるアプリの数を集計
app_counts_per_user_per_day = data.groupby(['user', 'days']).nunique()['app_name']

# 結果をデータフレームに変換
heatmap_data = app_counts_per_user_per_day.unstack(fill_value=0)

# ヒートマップを作成
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='viridis')
plt.title('Number of unique apps used per user per day')
plt.ylabel('User')
plt.xlabel('Day')
plt.tick_params(axis='y', rotation=0)
plt.savefig(output_path)
plt.close()