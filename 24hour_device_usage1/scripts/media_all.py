# media_all.py
# media.csvから24時間毎のPC,MB,TVのユーザー全員分の累計視聴時間をグラフ化する

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

media_data = pd.read_csv('../data/csv/media.csv', parse_dates=['start_viewing_date'])

media_data['viewing_start_time'] = media_data['start_viewing_date'].dt.hour

# 時間帯毎にメディア毎のviewing_durationの合計を計算
viewing_sum = media_data.groupby(['viewing_start_time', 'media'])['viewing_duration'].sum().unstack(fill_value=0)

sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(10, 6))

# メディアごとに異なる色で棒グラフをプロット
media_colors = sns.color_palette("Set2", n_colors=len(viewing_sum.columns))
for index, media in enumerate(viewing_sum.columns):
    ax.bar(viewing_sum.index + index * 0.2, viewing_sum[media], label=media, width=0.2, color=media_colors[index])

# 軸ラベルと凡例の設定
ax.set_xlabel('Hour of Day (0-23)')
ax.set_ylabel('Total Viewing Duration (seconds) (all users)')
ax.legend(title='Media')

# x軸のティックラベルを0から23まで設定
ax.set_xticks(np.arange(0, 24))
ax.set_xticklabels(np.arange(0, 24))

output_path = '../data/img/all/media_all.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
