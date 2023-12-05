#news_duration_heatmap.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

output_path = './img/Img_news_duration_heatmap.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

data = pd.read_csv('APP_add_days.csv', dtype={'user': str})

# 'ニュース'カテゴリのデータだけをフィルタリングする
news_data = data[data['app_category'] == 'ニュース']

# 日毎の利用時間の合計を計算する
daily_duration = news_data.groupby('days')['duration'].sum()

# 利用時間の合計を基に仮想的なヒートマップデータを作成する
heatmap_data = pd.DataFrame(daily_duration.values.reshape(-1, 1), 
                            index=daily_duration.index, 
                            columns=['Total Duration'])

# ヒートマップを作成する
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap='viridis') #annot=True: heatmapの各セルに値を表示。fmt=".0f": セルのアノテーションを整数値に。

# グラフのタイトルとラベルを設定する
plt.title('Daily Usage Duration of News Apps')
plt.xlabel('')
plt.ylabel('Days')
plt.tick_params(axis='y', rotation=0)

# レイアウトを調整する
plt.tight_layout()

plt.savefig(output_path)
plt.close()