#tool_news_duration_all.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import japanize_matplotlib
import os


data = pd.read_csv('./csv/APP_add_days.csv', dtype={'user': str})

# カテゴリごとにデータをフィルタリングして全ユーザーのグラフ化する関数
def plot_total_category_usage(category_name):
    # 特定のカテゴリのデータをフィルタリング
    category_data = data.loc[data['app_category'] == category_name].copy()

    # app_nameごとにdurationの合計を計算
    total_duration = category_data.groupby('app_name')['duration'].sum().reset_index()

    # アプリ名の文字数を適切な長さに制限
    total_duration['app_name'] = total_duration['app_name'].apply(lambda x: x[:12] + '...' if len(x) > 12 else x)

    # データをdurationで降順にソート
    total_duration.sort_values('duration', ascending=False, inplace=True)

    # グラフをプロット（xとyを入れ替えて横棒グラフにする）
    plt.figure(figsize=(8, 12))  # グラフのサイズを調整する
    bar_plot = sns.barplot(y='app_name', x='duration', data=total_duration, orient='h')  # orientを'h'に設定
    plt.yticks(rotation=0)  # y軸のラベルの回転を設定
    plt.title(f'全ユーザー - 「{category_name}」カテゴリのアプリ利用時間合計')
    plt.ylabel('アプリ名')  # xlabel と ylabel を入れ替える
    plt.xlabel('合計利用時間（秒）')
    plt.savefig(f'./img/tool_news/all/total_{category_name}_usage_horizontal_yx.png', bbox_inches='tight', dpi=300)
    plt.close()


# 'ツール類'カテゴリの全ユーザーの合計グラフを生成
plot_total_category_usage('ツール類')

# 'ニュース'カテゴリの全ユーザーの合計グラフを生成
plot_total_category_usage('ニュース')
