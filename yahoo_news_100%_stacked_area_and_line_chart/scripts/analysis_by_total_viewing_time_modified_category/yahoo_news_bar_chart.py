import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

df = pd.read_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time_modified_category.csv', dtype={'user': str})
category_list = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT', '科学', 'ライフ', '地域']

# データを加工
category_counts = df.groupby(['days', 'modified_category'])['viewing_time'].sum().unstack(fill_value=0).reindex(columns=category_list, fill_value=0)

# 全グラフ共通の設定
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
x_min = 1
x_max = 14
x_ticks = np.arange(x_min, x_max + 1)
x_labels = [f'Day {i}' for i in range(x_min, x_max + 1)]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)

# 線グラフを作成
category_colors = sns.color_palette("hls", n_colors=len(category_list))
category_counts.plot(kind='bar', stacked=True, color=category_colors, ax=ax)

ax.set_title('全ユーザー カテゴリー別日数の視聴時間')
ax.set_ylabel('視聴時間')
ax.set_xlabel('Days')

# x軸のティックとラベルを設定
x_ticks = np.arange(x_min, x_max + 1)  # 1から13までの数値
x_labels = [f'Day {i}' for i in x_ticks]  # 'Day 1' から 'Day 13' までのラベル

# グラフのx軸にティックとラベルを設定
ax.set_xticks(x_ticks - 1)  # ティックの位置を0ベースのインデックスに合わせる
ax.set_xticklabels(x_labels, rotation=45)

# x軸の範囲を設定
ax.set_xlim(-0.5, len(category_counts.index) - 0.5)

# 凡例の設定
handles, labels = plt.gca().get_legend_handles_labels()
handles = [handles[labels.index(cat)] for cat in category_list if cat in labels]
labels = [label for label in category_list if label in labels]
ax.legend(handles, labels, title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

output_path = '../../data/img/analysis_by_total_viewing_time_modified_category/bar_chart/all/bar_chart_modified.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
plt.close()
print(f'{output_path} was output.')
