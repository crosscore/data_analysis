# media_per_user_all.py
# media.csvから時間別のPC,MB,TVのユーザー毎の累計視聴時間をグラフ化する（1つのpngとして出力）
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

media_data = pd.read_csv('../data/csv/media.csv', parse_dates=['start_viewing_date'])

# viewing_start_timeという新しい列を作成し、各視聴開始日時の時間を抽出
media_data['viewing_start_time'] = media_data['start_viewing_date'].dt.hour

users = media_data['user'].unique()
users = users[:15] if len(users) > 15 else users

fig, axes = plt.subplots(5, 3, figsize=(15, 25))
# グリッドの各位置に対して、userごとのグラフを作成
for i, user in enumerate(users):
    ax = axes[i // 3, i % 3]
    user_data = media_data[media_data['user'] == user]
    viewing_sum = user_data.groupby(['viewing_start_time', 'media'])['viewing_duration'].sum().unstack(fill_value=0)
    
    # メディアごとに異なる色を使って棒グラフをプロット
    media_colors = sns.color_palette("Set2", n_colors=len(viewing_sum.columns))
    for index, media in enumerate(viewing_sum.columns):
        ax.bar(viewing_sum.index + index * 0.2, viewing_sum[media], label=media, width=0.2, color=media_colors[index])

    ax.set_xlim(-0.5, 24)  
    ax.set_ylim(0, 120000)
    ax.set_title(f'User: {user}')
    ax.set_xlabel('Hour of Day (0-23)')
    ax.set_ylabel('Total Viewing Duration (seconds)')
    ax.legend(title='Media')
    ax.set_xticks(np.arange(0, 24))
    ax.set_xticklabels(np.arange(0, 24))

plt.tight_layout()
output_path = '../data/img/per_user_all/per_user_all.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path)
