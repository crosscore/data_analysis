import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

df = pd.read_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time_modified_category.csv', dtype={'user': str})
category_list = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT', '科学', 'ライフ', '地域']

for user in df['user'].unique():
    user_df = df[df['user'] == user]

    # データを加工
    # 日付ごとにカテゴリのカウントを集計し、不足している日付の行を0で埋める
    category_counts = user_df.groupby(['days', 'modified_category'])['viewing_time'].sum().unstack(fill_value=0)
    category_counts = category_counts.reindex(index=days_range, columns=category_list, fill_value=0)

    # 全グラフ共通の設定
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    x_min = 1
    x_max = 14
    x_ticks = np.arange(x_min, x_max + 1)
    x_labels = [f'Day {i}' for i in range(x_min, x_max + 1)]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)

    # グラフを描画
    fig, ax = plt.subplots(figsize=(10, 6))

    # 棒グラフをプロット
    category_colors = sns.color_palette("hls", len(category_list))
    category_counts.plot(kind='bar', stacked=True, color=category_colors, ax=ax)

    # タイトルとラベルの設定
    ax.set_title(f'{user}のカテゴリー別の視聴時間')
    ax.set_xlabel('Days')
    ax.set_ylabel('視聴時間')

    # x軸のティックとラベルを設定
    x_ticks = np.arange(x_min, x_max + 1)  # 1から14までの数値
    x_labels = [f'Day {i}' for i in x_ticks]  # 'Day 1' から 'Day 14' までのラベル

    # 凡例の設定
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    output_path = f'../../data/img/analysis_by_total_viewing_time_modified_category/bar_chart/user/{user}_bar_chart_modified.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} was output.')
