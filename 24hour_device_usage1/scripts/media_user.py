import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

media_data = pd.read_csv('../data/csv/media.csv', parse_dates=['start_viewing_date'], dtype={'user': str})

# viewing_start_timeという新しい列を作成し、各視聴開始日時の時間を抽出
media_data['viewing_start_time'] = media_data['start_viewing_date'].dt.hour

# userの一覧を取得
users = media_data['user'].unique()
users = users[:15] if len(users) > 15 else users

for user in users:
    user_data = media_data[media_data['user'] == user]
    viewing_sum = user_data.groupby(['viewing_start_time', 'media'])['viewing_duration'].sum().unstack(fill_value=0)
    
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # メディアごとに異なる色で棒グラフをプロット
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
    
    output_path = f'../data/img/user/{user}.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    print(f'{user}.png was output.')
    plt.close(fig)
