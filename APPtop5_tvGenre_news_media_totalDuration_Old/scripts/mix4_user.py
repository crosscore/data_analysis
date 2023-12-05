import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

media_data = pd.read_csv('./csv/complete/Media.csv', dtype={'user': str})
device_data = pd.read_csv('./csv/complete/Device.csv', dtype={'user': str})
app_data = pd.read_csv('./csv/complete/APP.csv', dtype={'user': str})

# ユーザーIDのリストを取得
users = device_data['user'].unique()

for user in users:
    # ユーザーごとのデータをフィルタリング
    user_media_data = media_data[media_data['user'] == user]
    user_device_data = device_data[device_data['user'] == user]
    user_app_data = app_data[app_data['user'] == user]

    # deviceデータに関するグラフ描画の設定を継承
    device_counts = user_device_data.groupby(['days', 'device_id']).size().unstack(fill_value=0).reindex(columns=[0, 1, 2, 3], fill_value=0).reset_index()

    # appデータからニュースカテゴリの使用時間合計を計算
    news_app_data = user_app_data[user_app_data['app_category'] == 'ニュース']
    news_duration_by_day = news_app_data.groupby('days')['duration'].sum().reset_index()

    # appデータから各アプリの使用時間を計算し、上位5つとその他を抽出
    top_apps_duration_by_day = user_app_data.groupby(['days', 'app_name'])['duration'].sum().reset_index()
    top_apps_by_duration = top_apps_duration_by_day.groupby('app_name')['duration'].sum().sort_values(ascending=False)
    top_5_apps = top_apps_by_duration.head(5).index.tolist()
    top_apps_duration_by_day['app_category'] = top_apps_duration_by_day['app_name'].apply(lambda x: x if x in top_5_apps else 'others')
    top_apps_duration_by_day = top_apps_duration_by_day.groupby(['days', 'app_category'])['duration'].sum().reset_index()

    # Mediaデータのdurationの日毎の合計を計算
    media_duration_by_day = user_media_data.groupby(['days', 'media'])['duration'].sum().reset_index()

    # TVデータのジャンル別のdurationの日毎の合計を計算
    genre_duration_by_day = user_media_data[user_media_data['media'] == 'TV'].groupby(['days', 'genre_name'])['duration'].sum().unstack(fill_value=0).reset_index()

    # 全TVデータから全ジャンルを取得して固定順序リストを作成
    all_genres = user_media_data[user_media_data['media'] == 'TV']['genre_name'].unique()
    all_genres.sort()


    # 全グラフ共通の設定
    fig, axes = plt.subplots(5, 1, figsize=(10, 15), sharex=True)
    x_min = device_counts['days'].min()
    x_max = device_counts['days'].max()
    x_ticks = np.arange(x_min, x_max + 1)
    x_labels = [f'Day {i}' for i in range(x_min, x_max + 1)]
    for ax in axes:
        ax.set_xticks(x_ticks)
        ax.set_xticklabels(x_labels, rotation=45)

    # deviceのグラフ
    device_colors = sns.color_palette("muted", n_colors=4)
    width = 0.2
    for index, device_id in enumerate([0, 1, 2, 3]):
        axes[0].bar(device_counts['days'] + index * width, device_counts[device_id], width=width, color=device_colors[index], label=f'device_id {device_id}', align='edge')
    axes[0].set_title(f'user {user} device_id別 使用回数')
    axes[0].set_ylabel('使用回数')
    axes[0].legend(title='device_id', bbox_to_anchor=(1.05, 1), loc='upper left')

    # APP「ニュース」カテゴリ使用時間のグラフ
    app_colors = sns.color_palette("muted", n_colors=1)
    axes[1].bar(news_duration_by_day['days'], news_duration_by_day['duration'], width=0.8, align='edge', color=app_colors)
    axes[1].set_title(f'user {user} APP「ニュース」カテゴリ 累計視聴時間')
    axes[1].set_ylabel('使用時間 (秒)')

    # APP TOP5 + others カテゴリ使用時間のグラフ
    app_top5_colors = sns.color_palette("muted", n_colors=6)
    categories = top_apps_duration_by_day['app_category'].unique()
    categories_duration = top_apps_duration_by_day.groupby('app_category')['duration'].sum().sort_values(ascending=False)
    sorted_categories = categories_duration.index.tolist()
    category_to_index = {category: index for index, category in enumerate(sorted_categories)}
    for category in sorted_categories:
        category_data = top_apps_duration_by_day[top_apps_duration_by_day['app_category'] == category]
        offset = category_to_index[category] * 0.1
        axes[2].bar(category_data['days'] + offset, category_data['duration'], width=0.1, align='edge', label=category, color=app_top5_colors[category_to_index[category]])
    axes[2].set_title(f'user {user} APP TOP5+others 利用時間')
    axes[2].set_ylabel('使用時間 (秒)')
    handles, labels = axes[2].get_legend_handles_labels()
    sorted_handles_labels = sorted(zip(handles, labels), key=lambda x: categories_duration[x[1]], reverse=True)
    sorted_handles, sorted_labels = zip(*sorted_handles_labels)
    sorted_labels = [label if len(label) <= 15 else label[:12] + '...' for label in sorted_labels]
    axes[2].legend(sorted_handles, sorted_labels, title='app_name', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Mediaデータ (MB/PC) のグラフ
    media_types = ['MB', 'PC']
    media_colors = sns.color_palette("muted", n_colors=len(media_types))
    media_duration_by_type = media_data[media_data['media'].isin(media_types)].groupby(['days', 'media'])['duration'].sum().unstack(fill_value=0).reset_index()
    bar_width = 0.35
    for i, media_type in enumerate(media_types):
        axes[3].bar(media_duration_by_type['days'] + (i * bar_width), media_duration_by_type[media_type], width=bar_width, label=media_type, color=media_colors[i], align='edge')

    axes[3].set_title(f'user {user} Media (MB/PC) 使用時間')
    axes[3].set_ylabel('使用時間 (秒)')
    axes[3].legend(title='Media', bbox_to_anchor=(1.05, 1), loc='upper left')

    # TVジャンル別視聴時間グラフ
    num_genres = len(all_genres)
    tv_colors = sns.color_palette("muted", n_colors=len(all_genres))
    bar_width = 0.8 / num_genres
    genre_colors = sns.color_palette("RdPu", len(all_genres))
    for day in genre_duration_by_day['days']:
        day_genres = genre_duration_by_day[genre_duration_by_day['days'] == day]
        for i, genre in enumerate(all_genres):
            data = day_genres[genre].values[0] if genre in day_genres.columns else 0
            x_position = day + (i * bar_width)
            axes[4].bar(x_position, data, width=bar_width, label=genre if day == genre_duration_by_day['days'].min() else "", color=tv_colors[i], align='edge')
    axes[4].set_title(f'user {user} TVジャンル別 視聴時間')
    axes[4].set_ylabel('使用時間 (秒)')
    handles, labels = plt.gca().get_legend_handles_labels()
    handles = [handles[labels.index(genre)] for genre in all_genres if genre in labels]
    labels = [label for label in all_genres if label in labels]
    axes[4].legend(handles, labels, title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')

    output_path = f'./img/user/Img_mix4_{user}.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'Img_mix4_{user}.png was output.')
