import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

df = pd.read_csv('../data/csv/category_days.csv', dtype={'user': str})
category_list = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT', '科学', 'ライフ', '地域']

for user in df['user'].unique():
    user_df = df[df['user'] == user]
    # データを加工
    category_counts = user_df.groupby(['days', 'category']).size().unstack(fill_value=0).reindex(columns=category_list, fill_value=0)

    # 全グラフ共通の設定
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    x_min = 1
    x_max = 13
    x_ticks = np.arange(x_min, x_max + 1)
    x_labels = [f'Day {i}' for i in range(x_min, x_max + 1)]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)

    # 線グラフを作成
    category_colors = sns.color_palette("hls", n_colors=len(category_list))
    category_counts.plot(kind='line', color=category_colors, ax=ax)

    ax.set_title(f'{user}のカテゴリー別日数の視聴回数')
    ax.set_ylabel('視聴回数')
    ax.set_xlabel('Days')

    # x軸の設定
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)

    # x軸の範囲を設定
    ax.set_xlim(x_min, x_max)

    # 凡例の設定
    handles, labels = plt.gca().get_legend_handles_labels()
    handles = [handles[labels.index(cat)] for cat in category_list if cat in labels]
    labels = [label for label in category_list if label in labels]
    ax.legend(handles, labels, title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    # 画像の保存と閉じる
    output_path = f'../data/img/line_chart/user/{user}_line_chart.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} was output.')