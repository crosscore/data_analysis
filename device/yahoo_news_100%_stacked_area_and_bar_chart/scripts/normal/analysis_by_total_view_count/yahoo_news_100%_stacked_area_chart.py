#yahoo_news_100%_stacked_area_chart.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

df = pd.read_csv('../../../data/csv/add_viewing_time/device_add_days_viewing_time.csv', dtype={'user': str})
category_list = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT', '科学', 'ライフ', '地域']

# データを加工
category_totals = df.groupby(['days', 'category']).size().unstack(fill_value=0).reindex(columns=category_list, fill_value=0)

# 日付の範囲を確保
days_range = np.arange(1, 15)  # Day 1からDay 14まで
category_totals = category_totals.reindex(days_range, fill_value=0)  # 日付の範囲を設定

# 各カテゴリーの割合を計算（100% stacked area chartのため）
category_percentage = category_totals.div(category_totals.sum(axis=1), axis=0)

# 全グラフ共通の設定
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
x_ticks = days_range
x_labels = [f'Day {i}' for i in x_ticks]

# 100%積み上げ面グラフを作成
category_colors = sns.color_palette("hls", n_colors=len(category_list))
category_percentage.plot(kind='area', stacked=True, color=category_colors, ax=ax)

ax.set_title('全ユーザー カテゴリー別視聴回数の割合')
ax.set_ylabel('割合')
ax.set_xlabel('Days')

# x軸のティックとラベルを設定
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)

# x軸の範囲を設定
ax.set_xlim(days_range[0], days_range[-1])

# 凡例を設定
handles, labels = ax.get_legend_handles_labels()
handles = [handles[labels.index(cat)] for cat in category_list if cat in labels]
labels = [label for label in category_list if label in labels]
ax.legend(handles, labels, title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

output_path = '../../../data/img/normal/analysis_by_total_view_count/100%_stacked_area_chart/all/stacked_area_chart.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
plt.close()
print(f'{output_path} was output.')
