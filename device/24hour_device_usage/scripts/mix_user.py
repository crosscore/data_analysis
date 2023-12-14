import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import os

device_data = pd.read_csv('../data/csv/device.csv', parse_dates=['start_viewing_date'], dtype={'user': str})
media_data = pd.read_csv('../data/csv/media.csv', parse_dates=['start_viewing_date'], dtype={'user': str})

# 日付の範囲を設定
date_min = pd.to_datetime('2022-10-22')
date_max = pd.to_datetime('2022-12-16')

# ユーザーのリストを取得
user_list = device_data['user'].unique()

def format_xaxis(ax):
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  # 毎日の目盛りを設定
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d-%a'))  # 日付と曜日を表示
    ax.tick_params(axis='x', rotation=270)  # x軸のラベルの回転をリセット
    # 土曜日と日曜日のラベルの色を変更
    for label in ax.get_xticklabels():
        label_text = label.get_text()
        if label_text.endswith('-Sat'):
            label.set_color('darkblue')
        elif label_text.endswith('-Sun'):
            label.set_color('crimson')

for user in user_list:
    ### dfの編集 ###
    # ユーザー毎のdfを新たに作成
    user_device_data = device_data[device_data['user'] == user].copy()
    user_media_data = media_data[media_data['user'] == user].copy()

    ## device_data ##
    # device_data: 'date'列、'device_id'列を追加＆編集
    user_device_data['date'] = user_device_data['start_viewing_date'].dt.date
    user_device_data['device_id'] = user_device_data['device_id'].astype(str)  # device_idを文字列に変換
    device_counts = user_device_data.groupby(['date', 'device_id']).size().unstack(fill_value=0).reset_index()
    device_counts = device_counts.reindex(columns=['date', '0', '1', '2', '3'], fill_value=0)  # reindexを使用して列の順序と存在を保証

    ## media_data ##
    # media_data: 'date'列を追加
    user_media_data['date'] = user_media_data['start_viewing_date'].dt.date
    media_sum = user_media_data.groupby(['date', 'media'])['viewing_duration'].sum().unstack(fill_value=0).reset_index()
    media_sum = media_sum.reindex(columns=['date', 'MB', 'PC', 'TV'], fill_value=0)  # reindexを使用して列の順序と存在を保証

    device_counts['date'] = pd.to_datetime(device_counts['date'])
    media_sum['date'] = pd.to_datetime(media_sum['date'])

    ### グラフの作成 ###
    sns.set(style="darkgrid")
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))  # 2つのグラフを上下に配置

    # 色の設定
    device_colors = sns.color_palette("Set1", n_colors=len(device_counts.columns[1:]))
    media_colors = sns.color_palette("Set2", n_colors=len(media_sum.columns[1:]))

    ## deviceのグラフ ##
    axes[0].set_xlim([date_min, date_max])  # x軸の範囲を設定
    width = 0.2  # バーの幅を設定
    for index, device_id in enumerate(device_counts.columns[1:]):
        axes[0].bar(device_counts['date'] + pd.to_timedelta(index * width, unit='D'), device_counts[device_id], label=device_id,
                    width=width, color=device_colors[index])

    axes[0].set_xlabel('')
    axes[0].set_ylabel(f'View count (user {user})')
    format_xaxis(axes[0])  # 日時のフォーマットを変更
    axes[0].legend(title='device_id')

    ## mediaのグラフ ##
    axes[1].set_xlim([date_min, date_max])
    width = 0.2666
    for index, media in enumerate(media_sum.columns[1:]):
        axes[1].bar(media_sum['date'] + pd.to_timedelta(index * width, unit='D'), media_sum[media], label=media, width=width, 
                    color=media_colors[index])
    axes[1].set_xlabel('Date')
    axes[1].set_ylabel(f'Total viewing time (seconds) (user {user})')
    format_xaxis(axes[1])
    axes[1].legend(title='media')

    ### output ###
    output_path = f'../data/img/user/Img_mix_{user}.png'
    print(f'Img_mix_{user}.png was output.')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
