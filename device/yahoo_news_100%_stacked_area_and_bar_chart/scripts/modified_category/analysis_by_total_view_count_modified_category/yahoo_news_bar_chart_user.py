import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

df = pd.read_csv('../../data/csv/add_days/device_add_days_modified_category.csv', dtype={'user': str})
category_list = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT', '科学', 'ライフ', '地域']

for user in df['user'].unique():
    user_df = df[df['user'] == user]
    
    # グラフに表示する日付の範囲を指定
    days_range = np.arange(1, 15)  # 1から14までの日付
    
    # データを加工
    # 日付ごとにカテゴリのカウントを集計し、不足している日付の行を0で埋める
    category_totals = user_df.groupby(['days', 'modified_category']).size().unstack(fill_value=0)
    category_totals = category_totals.reindex(index=days_range, columns=category_list, fill_value=0)
    
    # グラフを描画
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 棒グラフをプロット
    category_colors = sns.color_palette("hls", len(category_list))
    category_totals.plot(kind='bar', stacked=True, color=category_colors, ax=ax)
    
    # タイトルとラベルの設定
    ax.set_title(f'{user}のカテゴリー別日数の視聴回数')
    ax.set_xlabel('Days')
    ax.set_ylabel('視聴回数')
    ax.set_xticks(np.arange(len(days_range)))
    ax.set_xticklabels([f'Day {i}' for i in days_range], rotation=45)
    
    # 凡例の設定
    ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    output_path = f'../../data/img/analysis_by_total_view_count_modified_category/bar_chart/user/{user}_bar_chart_modified.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} was output.')
