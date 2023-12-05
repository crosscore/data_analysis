#news_duration_bar.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

output_path = './img/Img_news_duration_bar.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
data = pd.read_csv('APP_add_days.csv', dtype={'user': str})

# 'ニュース'カテゴリのデータだけをフィルタリングする
news_data = data[data['app_category'] == 'ニュース']

# 日毎の利用時間の合計を計算する
daily_duration = news_data.groupby('days')['duration'].sum()

# スタイルとコンテキストを設定する
sns.set_style('whitegrid')
sns.set_context('talk')

# 日毎の利用時間の合計に基づいて色の順序を決定する
rank = daily_duration.values.argsort().argsort()
colors = sns.color_palette("viridis_r", len(daily_duration)).as_hex()  # カラーパレットをhex形式のリストに変換
ordered_colors = [colors[i] for i in rank]  # 色の順序を変更

# グラフを作成する
sns.barplot(x=daily_duration.index, y=daily_duration.values, palette=ordered_colors, hue=daily_duration.index, legend=False)

# タイトルとラベルを設定する
plt.title('Daily Usage Duration of News Apps')
plt.xlabel('Days')
plt.ylabel('Total Duration')

# レイアウトを調整する
plt.tight_layout()

plt.savefig(output_path)
plt.close()