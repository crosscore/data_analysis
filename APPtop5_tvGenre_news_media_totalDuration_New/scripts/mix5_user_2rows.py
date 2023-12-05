#mix5_user_2rows.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

app_data = pd.read_csv('../data/csv/complete/APP_1st.csv', dtype={'user': str})
device_data = pd.read_csv('../data/csv/complete/Device_1st.csv', dtype={'user': str})
media_data = pd.read_csv('../data/csv/complete/Media_1st.csv', dtype={'user': str})
app_data_2nd = pd.read_csv('../data/csv/complete/APP_2nd.csv', dtype={'user': str})
device_data_2nd = pd.read_csv('../data/csv/complete/Device_2nd.csv', dtype={'user': str})
media_data_2nd = pd.read_csv('../data/csv/complete/Media_2nd.csv', dtype={'user': str})

# ラベル文字数制限
def trim_label(label, max_length=18):
    return label if len(label) <= max_length else label[:max_length] + '...'

users = app_data['user'].unique()

for user in users:
    print(f'Start processing data for user {user}')
    user_app_data = app_data[app_data['user'] == user]
    user_device_data = device_data[device_data['user'] == user]
    user_media_data = media_data[media_data['user'] == user]
    user_app_data_2nd = app_data_2nd[app_data_2nd['user'] == user]
    user_device_data_2nd = device_data_2nd[device_data_2nd['user'] == user]
    user_media_data_2nd = media_data_2nd[media_data_2nd['user'] == user]

    # 1stデータセットに対するデータ処理のコード
    # deviceデータに関するグラフ描画設定
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
    all_genre = user_media_data[user_media_data['media'] == 'TV']['genre_name'].unique()
    all_genre.sort()


    # 2ndデータセットに対するデータ処理のコード
    # deviceデータに関するグラフ描画設定（2ndデータセット）
    device_counts_2nd = user_device_data_2nd.groupby(['days', 'device_id']).size().unstack(fill_value=0).reindex(columns=[0, 1, 2, 3], fill_value=0).reset_index()

    # appデータからニュースカテゴリの使用時間合計を計算（2ndデータセット）
    news_app_data_2nd = user_app_data_2nd[user_app_data_2nd['app_category'] == 'ニュース']
    news_duration_by_day_2nd = news_app_data_2nd.groupby('days')['duration'].sum().reset_index()

    # appデータから各アプリの使用時間を計算し、上位5つとその他を抽出（2ndデータセット）
    top_apps_duration_by_day_2nd = user_app_data_2nd.groupby(['days', 'app_name'])['duration'].sum().reset_index()
    top_apps_by_duration_2nd = top_apps_duration_by_day_2nd.groupby('app_name')['duration'].sum().sort_values(ascending=False)
    top_5_apps_2nd = top_apps_by_duration_2nd.head(5).index.tolist()
    top_apps_duration_by_day_2nd['app_category'] = top_apps_duration_by_day_2nd['app_name'].apply(lambda x: x if x in top_5_apps_2nd else 'others')
    top_apps_duration_by_day_2nd = top_apps_duration_by_day_2nd.groupby(['days', 'app_category'])['duration'].sum().reset_index()

    # Mediaデータのdurationの日毎の合計を計算（2ndデータセット）
    media_duration_by_day_2nd = user_media_data_2nd.groupby(['days', 'media'])['duration'].sum().reset_index()
    # TVデータのジャンル別のdurationの日毎の合計を計算（2ndデータセット）
    genre_duration_by_day_2nd = user_media_data_2nd[user_media_data_2nd['media'] == 'TV'].groupby(['days', 'genre_name'])['duration'].sum().unstack(fill_value=0).reset_index()
    # 全TVデータから全ジャンルを取得して固定順序リストを作成（2ndデータセット）
    all_genre_2nd = user_media_data_2nd[user_media_data_2nd['media'] == 'TV']['genre_name'].unique()
    all_genre_2nd.sort()



    # 全グラフ共通の設定を5行2列に変更
    fig, axes = plt.subplots(5, 2, figsize=(20, 15), sharex='col')

    # x軸の共通設定
    x_min = 1
    x_max = 14
    x_ticks = np.arange(x_min, x_max + 1)
    x_labels = [f'Day {i}' for i in range(x_min, x_max + 1)]


    # deviceのグラフ（1stデータセット）
    ax = axes[0, 0]
    print(ax)
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    device_colors = sns.color_palette("muted", n_colors=4)
    width = 0.2
    for index, device_id in enumerate([0, 1, 2, 3]):
        ax.bar(device_counts['days'] + index * width, device_counts[device_id], width=width, color=device_colors[index], label=f'device_id {device_id}', align='edge')
    ax.set_title(f'user {user} device_id別 使用回数（1stデータセット）')
    ax.set_ylabel('使用回数')
    #ax.legend(title='device_id', bbox_to_anchor=(1.05, 1), loc='upper left')

    # APP「ニュース」カテゴリ使用時間のグラフ（1stデータセット）
    ax = axes[1, 0]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    app_colors = sns.color_palette("muted", n_colors=1)
    ax.bar(news_duration_by_day['days'], news_duration_by_day['duration'], width=0.8, align='edge', color=app_colors)
    ax.set_title(f'user {user} APP「ニュース」カテゴリ 累計視聴時間（1stデータセット）')
    ax.set_ylabel('使用時間 (秒)')

    # APP TOP5 + others カテゴリ使用時間のグラフ（1stデータセット）
    ax = axes[2, 0]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    app_top5_colors = sns.color_palette("muted", n_colors=6)
    sorted_categories = top_apps_duration_by_day['app_category'].unique()
    categories_duration = top_apps_duration_by_day.groupby('app_category')['duration'].sum().sort_values(ascending=False)
    sorted_categories = categories_duration.index.tolist()
    category_to_index = {category: index for index, category in enumerate(sorted_categories)}
    for category in sorted_categories:
        category_data = top_apps_duration_by_day[top_apps_duration_by_day['app_category'] == category]
        offset = category_to_index[category] * 0.1
        trimmed_label = trim_label(category)
        ax.bar(category_data['days'] + offset, category_data['duration'], width=0.1, align='edge', label=trimmed_label, color=app_top5_colors[category_to_index[category]])
    ax.set_title(f'user {user} APP TOP5+others 利用時間（1stデータセット）')
    ax.set_ylabel('使用時間 (秒)')
    ax.legend(title='app_name', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Mediaデータ (MB/PC) のグラフ（1stデータセット）
    ax = axes[3, 0]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    media_types = ['MB', 'PC']
    media_colors = sns.color_palette("muted", n_colors=len(media_types))
    media_duration_by_type = media_data[media_data['media'].isin(media_types)].groupby(['days', 'media'])['duration'].sum().unstack(fill_value=0).reset_index()
    for media_type in ['MB', 'PC']:
        if media_type not in media_duration_by_type:
            media_duration_by_type[media_type] = 0
    bar_width = 0.35
    for i, media_type in enumerate(media_types):
        ax.bar(media_duration_by_type['days'] + (i * bar_width), media_duration_by_type[media_type], width=bar_width, label=media_type, color=media_colors[i], align='edge')
    ax.set_title(f'user {user} Media (MB/PC) 使用時間（1stデータセット）')
    ax.set_ylabel('使用時間 (秒)')
    ax.legend(title='Media', bbox_to_anchor=(1.05, 1), loc='upper left')

    # TVジャンル別視聴時間グラフ（1stデータセット）
    ax = axes[4, 0]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    num_genres = len(all_genre)
    tv_colors = sns.color_palette("muted", n_colors=len(all_genre))
    if num_genres == 0:
        bar_width = 0.8
    else:
        bar_width = 0.8 / num_genres
    for day in genre_duration_by_day['days']:
        day_genres = genre_duration_by_day[genre_duration_by_day['days'] == day]
        for i, genre in enumerate(all_genre):
            data = day_genres[genre].values[0] if genre in day_genres.columns else 0
            x_position = day + (i * bar_width)
            ax.bar(x_position, data, width=bar_width, label=genre if day == genre_duration_by_day['days'].min() else "", color=tv_colors[i], align='edge')
    ax.set_title(f'user {user} TVジャンル別 視聴時間（1stデータセット）')
    ax.set_ylabel('使用時間 (秒)')
    if num_genres > 0:
        ax.legend(all_genre, title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')


    # Deviceのグラフ（2ndデータセット）
    ax = axes[0, 1]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    device_colors = sns.color_palette("muted", n_colors=4)
    width = 0.2
    for index, device_id in enumerate([0, 1, 2, 3]):
        ax.bar(device_counts_2nd['days'] + index * width, device_counts_2nd[device_id], width=width, color=device_colors[index], label=f'device_id {device_id}', align='edge')
    ax.set_title(f'user {user} device_id別 使用回数（2ndデータセット）')
    ax.set_ylabel('使用回数')
    ax.legend(title='device_id', bbox_to_anchor=(1.05, 1), loc='upper left')

    # APP「ニュース」カテゴリ使用時間のグラフ（2ndデータセット）
    ax = axes[1, 1]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    app_colors = sns.color_palette("muted", n_colors=1)
    ax.bar(news_duration_by_day_2nd['days'], news_duration_by_day_2nd['duration'], width=0.8, align='edge', color=app_colors)
    ax.set_title(f'user {user} APP「ニュース」カテゴリ 累計視聴時間（2ndデータセット）')
    ax.set_ylabel('使用時間 (秒)')

    # APP TOP5 + others カテゴリ使用時間のグラフ（2ndデータセット）
    ax = axes[2, 1]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    app_top5_colors = sns.color_palette("muted", n_colors=6)
    sorted_categories = top_apps_duration_by_day_2nd['app_category'].unique()
    categories_duration = top_apps_duration_by_day_2nd.groupby('app_category')['duration'].sum().sort_values(ascending=False)
    sorted_categories = categories_duration.index.tolist()
    category_to_index = {category: index for index, category in enumerate(sorted_categories)}
    for category in sorted_categories:
        category_data = top_apps_duration_by_day_2nd[top_apps_duration_by_day_2nd['app_category'] == category]
        offset = category_to_index[category] * 0.1
        trimmed_label = trim_label(category)
        ax.bar(category_data['days'] + offset, category_data['duration'], width=0.1, align='edge', label=trimmed_label, color=app_top5_colors[category_to_index[category]])
    ax.set_title(f'user {user} APP TOP5+others 利用時間（2ndデータセット）')
    ax.set_ylabel('使用時間 (秒)')
    ax.legend(title='app_name', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Mediaデータ (MB/PC) のグラフ（2ndデータセット）
    ax = axes[3, 1]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    media_types = ['MB', 'PC']
    media_colors = sns.color_palette("muted", n_colors=len(media_types))
    media_duration_by_type = media_data_2nd[media_data_2nd['media'].isin(media_types)].groupby(['days', 'media'])['duration'].sum().unstack(fill_value=0).reset_index()
    for media_type in ['MB', 'PC']:
        if media_type not in media_duration_by_type:
            media_duration_by_type[media_type] = 0
    bar_width = 0.35
    for i, media_type in enumerate(media_types):
        ax.bar(media_duration_by_type['days'] + (i * bar_width), media_duration_by_type[media_type], width=bar_width, label=media_type, color=media_colors[i], align='edge')
    ax.set_title(f'user {user} Media (MB/PC) 使用時間（2ndデータセット）')
    ax.set_ylabel('使用時間 (秒)')
    ax.legend(title='Media', bbox_to_anchor=(1.05, 1), loc='upper left')

    # TVジャンル別視聴時間グラフ（2データセット）
    ax = axes[4, 1]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)
    num_genres = len(all_genre_2nd)
    tv_colors = sns.color_palette("muted", n_colors=len(all_genre_2nd))
    if num_genres == 0:
        bar_width = 0.8
    else:
        bar_width = 0.8 / num_genres
    for day in genre_duration_by_day_2nd['days']:
        day_genres = genre_duration_by_day_2nd[genre_duration_by_day_2nd['days'] == day]
        for i, genre in enumerate(all_genre_2nd):
            data = day_genres[genre].values[0] if genre in day_genres.columns else 0
            x_position = day + (i * bar_width)
            ax.bar(x_position, data, width=bar_width, label=genre if day == genre_duration_by_day_2nd['days'].min() else "", color=tv_colors[i], align='edge')
    ax.set_title(f'user {user} TVジャンル別 視聴時間（2ndデータセット）')
    ax.set_ylabel('使用時間 (秒)')
    if num_genres > 0:
        ax.legend(all_genre_2nd, title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')


    # 左右のグラフのy軸の最大値を動的に計算する
    for i in range(5):
        left_max = max(axes[i,0].get_ylim())
        right_max = max(axes[i,1].get_ylim())
        ymax = max(left_max, right_max) * 1.05
        axes[i,0].set_ylim(0, ymax)
        axes[i,1].set_ylim(0, ymax)


    output_path = f'../data/img/user/Img_mix5_{user}_2rows.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'Img_mix5_{user}_2rows.png was output.')
