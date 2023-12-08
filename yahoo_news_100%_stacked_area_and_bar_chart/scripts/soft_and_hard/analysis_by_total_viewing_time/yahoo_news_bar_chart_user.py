#yahoo_news_bar_chart_user.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

df = pd.read_csv('../../../data/csv/add_viewing_time/device_add_days_viewing_time_soft_hard.csv', dtype={'user': str})
#category_list = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT', '科学', 'ライフ', '地域']
category_list = ['soft_news', 'hard_news']

for user in df['user'].unique():
    user_df = df[df['user'] == user]

    # データを加工
    category_totals = user_df.groupby(['days', 'category'])['viewing_time'].sum().unstack(fill_value=0).reindex(columns=category_list, fill_value=0)

    # 日付の範囲を確保
    days_range = np.arange(1, 15)  # Day 1からDay 14まで
    category_totals = category_totals.reindex(days_range, fill_value=0)  # 日付の範囲を設定

    # 全グラフ共通の設定
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    x_ticks = days_range
    x_labels = [f'Day {i}' for i in x_ticks]

    # 合計視聴時間を使用して棒グラフを作成
    category_colors = sns.color_palette("hls", n_colors=len(category_list))
    category_totals.plot(kind='bar', stacked=True, color=category_colors, ax=ax)

    ax.set_title(f'User {user} カテゴリー別視聴時間')
    ax.set_ylabel('視聴時間')
    ax.set_xlabel('Days')

    # x軸のティックとラベルを設定
    ax.set_xticks(x_ticks - 1)
    ax.set_xticklabels(x_labels, rotation=45)

    # x軸の範囲を設定
    ax.set_xlim(-0.5, len(days_range) - 0.5)

    # 凡例を設定
    handles, labels = ax.get_legend_handles_labels()
    handles = [handles[labels.index(cat)] for cat in category_list if cat in labels]
    labels = [label for label in category_list if label in labels]
    ax.legend(handles, labels, title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    output_path = f'../../../data/img/soft_and_hard/analysis_by_total_viewing_time/bar_chart/user/{user}_bar_chart.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} was output.')

