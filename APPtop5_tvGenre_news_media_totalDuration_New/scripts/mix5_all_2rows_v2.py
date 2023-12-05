#mix5_all_2rows_v2.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

app_data_1st = pd.read_csv('../data/csv/complete/APP_1st.csv', dtype={'user': str})
device_data_1st = pd.read_csv('../data/csv/complete/Device_1st.csv', dtype={'user': str})
media_data_1st = pd.read_csv('../data/csv/complete/Media_1st.csv', dtype={'user': str})
app_data_2nd = pd.read_csv('../data/csv/complete/APP_2nd.csv', dtype={'user': str})
device_data_2nd = pd.read_csv('../data/csv/complete/Device_2nd.csv', dtype={'user': str})
media_data_2nd = pd.read_csv('../data/csv/complete/Media_2nd.csv', dtype={'user': str})

# ラベルの文字数制限
def trim_label(label, max_length=18):
    return label if len(label) <= max_length else label[:max_length] + '...'

# category列追加用辞書 (media_data用)
new_categories = {
    'エンタメ': ['ドキュメンタリー', 'アニメ/特撮', '映画', '音楽', '演劇/公演', 'バラエティー', 'ドラマ'],
    'ニュース': ['ニュース/報道', '情報/ワイドショー'],
    'スポーツ': ['スポーツ'],
    '生活': ['趣味/教育', '福祉']
}
# 凡例用のカテゴリリストを作成
palette_name = 'muted'
legend_categories = list(new_categories)
legend_categories.sort()
category_colors = sns.color_palette(palette_name, n_colors=len(legend_categories))
category_color_dict = dict(zip(legend_categories, category_colors))

def map_genre_to_category(genre):
    for category, genres in new_categories.items():
        if genre in genres:
            return category
    return np.nan

media_data_1st['category'] = media_data_1st['genre_name'].apply(map_genre_to_category)
media_data_2nd['category'] = media_data_2nd['genre_name'].apply(map_genre_to_category)


# APPの両グラフ作成のため、1stと2nd両期間の上位5つの'app_name'を計算
app_data_total = pd.concat([app_data_1st, app_data_2nd])
top_5_apps_total = app_data_total.groupby('app_name')['duration'].sum().sort_values(ascending=False).head(5).index.tolist()


# deviceデータに関するグラフ描画設定（1stデータセット）
device_counts_1st = device_data_1st.groupby(['days', 'device_id']).size().unstack(fill_value=0).reindex(columns=[0, 1, 2, 3], fill_value=0).reset_index()

# appデータからニュースカテゴリの使用時間合計を計算（1stデータセット）
news_app_data_1st = app_data_1st[app_data_1st['app_category'] == 'ニュース']
news_duration_by_day_1st = news_app_data_1st.groupby('days')['duration'].sum().reset_index()

# appデータから各アプリの使用時間を計算し、上位5つとその他を抽出（1stデータセット）
top_apps_duration_by_day_1st = app_data_1st.groupby(['days', 'app_name'])['duration'].sum().reset_index()
top_apps_duration_by_day_1st['app_category'] = top_apps_duration_by_day_1st['app_name'].apply(lambda x: x if x in top_5_apps_total else 'others')
top_apps_duration_by_day_1st = top_apps_duration_by_day_1st.groupby(['days', 'app_category'])['duration'].sum().reset_index()

# TVデータのジャンル別のdurationの日毎の合計を計算（1stデータセット）
category_duration_by_day_1st = media_data_1st[media_data_1st['media'] == 'TV'].groupby(['days', 'category'])['duration'].sum().unstack(fill_value=0).reset_index()


# deviceデータに関するグラフ描画設定（2ndデータセット）
device_counts_2nd = device_data_2nd.groupby(['days', 'device_id']).size().unstack(fill_value=0).reindex(columns=[0, 1, 2, 3], fill_value=0).reset_index()

# appデータからニュースカテゴリの使用時間合計を計算（2ndデータセット）
news_app_data_2nd = app_data_2nd[app_data_2nd['app_category'] == 'ニュース']
news_duration_by_day_2nd = news_app_data_2nd.groupby('days')['duration'].sum().reset_index()

# appデータから各アプリの使用時間を計算し、上位5つとその他を抽出（2ndデータセット）
top_apps_duration_by_day_2nd = app_data_2nd.groupby(['days', 'app_name'])['duration'].sum().reset_index()
top_apps_duration_by_day_2nd['app_category'] = top_apps_duration_by_day_2nd['app_name'].apply(lambda x: x if x in top_5_apps_total else 'others')
top_apps_duration_by_day_2nd = top_apps_duration_by_day_2nd.groupby(['days', 'app_category'])['duration'].sum().reset_index()

# TVデータのジャンル別のdurationの日毎の合計を計算（2ndデータセット）
category_duration_by_day_2nd = media_data_2nd[media_data_2nd['media'] == 'TV'].groupby(['days', 'category'])['duration'].sum().unstack(fill_value=0).reset_index()


# 全グラフ共通の設定を5行2列に変更
fig, axes = plt.subplots(5, 2, figsize=(20, 15), sharex='col')

# x軸の共通設定
x_min = 1
x_max = 14
x_ticks = np.arange(x_min, x_max + 1)
x_labels = [f'Day {i}' for i in range(x_min, x_max + 1)]


# deviceのグラフ（1stデータセット ※データ無し）
ax = axes[0, 0]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
ax.set_xlim(x_min - 1, x_max + 1.5)
device_colors = sns.color_palette(palette_name, n_colors=4)
width = 0.2
for index, device_id in enumerate([0, 1, 2, 3]):
    ax.bar(device_counts_1st['days'] + index * width, device_counts_1st[device_id], width=width, color=device_colors[index], label=f'device_id {device_id}', align='edge')
ax.set_title(f'全ユーザー device_id別 使用回数（1stデータセット ※データ無し）')
ax.set_ylabel('使用回数')
ax.legend(title='device_id', bbox_to_anchor=(1.05, 1), loc='upper left')

# APP「ニュース」カテゴリ使用時間のグラフ（1stデータセット）
ax = axes[1, 0]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
app_colors = sns.color_palette(palette_name, n_colors=1)
ax.bar(news_duration_by_day_1st['days'], news_duration_by_day_1st['duration'], width=0.8, align='edge', color=app_colors)
ax.set_title(f'全ユーザー APP「ニュース」カテゴリ 累計視聴時間（1stデータセット）')
ax.set_ylabel('使用時間 (秒)')

# APP TOP5 + others カテゴリ使用時間のグラフ（1stデータセット）
ax = axes[2, 0]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
app_top5_colors = sns.color_palette(palette_name, n_colors=6)
sorted_categories = top_apps_duration_by_day_1st['app_category'].unique()
categories_duration = top_apps_duration_by_day_1st.groupby('app_category')['duration'].sum().sort_values(ascending=False)
sorted_categories = categories_duration.index.tolist()
category_to_index = {category: index for index, category in enumerate(sorted_categories)}
for category in sorted_categories:
    category_data = top_apps_duration_by_day_1st[top_apps_duration_by_day_1st['app_category'] == category]
    offset = category_to_index[category] * 0.133
    trimmed_label = trim_label(category)
    ax.bar(category_data['days'] + offset, category_data['duration'], width=0.133, align='edge', label=trimmed_label, color=app_top5_colors[category_to_index[category]])
ax.set_title(f'全ユーザー APP TOP5+others 利用時間（1stデータセット）')
ax.set_ylabel('使用時間 (秒)')
ax.legend(title='app_name', bbox_to_anchor=(1.05, 1), loc='upper left')

# Mediaデータ (MB/PC) のグラフ（1stデータセット）
ax = axes[3, 0]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
media_types = ['MB', 'PC']
media_colors = sns.color_palette(palette_name, n_colors=len(media_types))
media_duration_by_type = media_data_1st[media_data_1st['media'].isin(media_types)].groupby(['days', 'media'])['duration'].sum().unstack(fill_value=0).reset_index()
if 'MB' not in media_duration_by_type.columns:
    media_duration_by_type['MB'] = 0
if 'PC' not in media_duration_by_type.columns:
    media_duration_by_type['PC'] = 0
bar_width = 0.35
for i, media_type in enumerate(media_types):
    ax.bar(media_duration_by_type['days'] + (i * bar_width), media_duration_by_type[media_type], width=bar_width, label=media_type, color=media_colors[i], align='edge')
ax.set_title(f'全ユーザー Media (MB/PC) 使用時間（1stデータセット）')
ax.set_ylabel('使用時間 (秒)')
ax.legend(title='Media', bbox_to_anchor=(1.05, 1), loc='upper left')

# TVジャンル別視聴時間グラフの描画（1stデータセット）
ax = axes[4, 0]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
bar_width = 0.8 / len(legend_categories)
for i, category in enumerate(legend_categories):
    category_color = category_color_dict[category]
    # 凡例用のバー（非表示）を追加
    ax.bar(0, 0, width=bar_width, color=category_color, label=category)
    # 実際のデータがある場合のみバーをプロット
    if category in category_duration_by_day_1st.columns:
        ax.bar(category_duration_by_day_1st['days'] + i * bar_width, category_duration_by_day_1st[category], width=bar_width, color=category_color, align='edge')
ax.set_title(f'全ユーザー TVジャンル別 視聴時間（1stデータセット）')
ax.set_ylabel('使用時間 (秒)')
ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')


# Deviceのグラフ（2ndデータセット）
ax = axes[0, 1]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
ax.set_xlim(x_min - 1, x_max + 1.5)
device_colors = sns.color_palette(palette_name, n_colors=4)
width = 0.2
for index, device_id in enumerate([0, 1, 2, 3]):
    ax.bar(device_counts_2nd['days'] + index * width, device_counts_2nd[device_id], width=width, color=device_colors[index], label=f'device_id {device_id}', align='edge')
ax.set_title(f'全ユーザー device_id別 使用回数（2ndデータセット）')
ax.set_ylabel('使用回数')
ax.legend(title='device_id', bbox_to_anchor=(1.05, 1), loc='upper left')

# APP「ニュース」カテゴリ使用時間のグラフ（2ndデータセット）
ax = axes[1, 1]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
app_colors = sns.color_palette(palette_name, n_colors=1)
ax.bar(news_duration_by_day_2nd['days'], news_duration_by_day_2nd['duration'], width=0.8, align='edge', color=app_colors)
ax.set_title(f'全ユーザー APP「ニュース」カテゴリ 累計視聴時間（2ndデータセット）')
ax.set_ylabel('使用時間 (秒)')

# APP TOP5 + others カテゴリ使用時間のグラフ（2ndデータセット）
ax = axes[2, 1]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
app_top5_colors = sns.color_palette(palette_name, n_colors=6)
sorted_categories = top_apps_duration_by_day_2nd['app_category'].unique()
categories_duration = top_apps_duration_by_day_2nd.groupby('app_category')['duration'].sum().sort_values(ascending=False)
sorted_categories = categories_duration.index.tolist()
category_to_index = {category: index for index, category in enumerate(sorted_categories)}
for category in sorted_categories:
    category_data = top_apps_duration_by_day_2nd[top_apps_duration_by_day_2nd['app_category'] == category]
    offset = category_to_index[category] * 0.133
    trimmed_label = trim_label(category)
    ax.bar(category_data['days'] + offset, category_data['duration'], width=0.133, align='edge', label=trimmed_label, color=app_top5_colors[category_to_index[category]])
ax.set_title(f'全ユーザー APP TOP5+others 利用時間（2ndデータセット）')
ax.set_ylabel('使用時間 (秒)')
ax.legend(title='app_name', bbox_to_anchor=(1.05, 1), loc='upper left')

# Mediaデータ (MB/PC) のグラフ（2ndデータセット）
ax = axes[3, 1]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
media_types = ['MB', 'PC']
media_colors = sns.color_palette(palette_name, n_colors=len(media_types))
media_duration_by_type = media_data_2nd[media_data_2nd['media'].isin(media_types)].groupby(['days', 'media'])['duration'].sum().unstack(fill_value=0).reset_index()
if 'MB' not in media_duration_by_type.columns:
    media_duration_by_type['MB'] = 0
if 'PC' not in media_duration_by_type.columns:
    media_duration_by_type['PC'] = 0
bar_width = 0.35
for i, media_type in enumerate(media_types):
    ax.bar(media_duration_by_type['days'] + (i * bar_width), media_duration_by_type[media_type], width=bar_width, label=media_type, color=media_colors[i], align='edge')
ax.set_title(f'全ユーザー Media (MB/PC) 使用時間（2ndデータセット）')
ax.set_ylabel('使用時間 (秒)')
ax.legend(title='Media', bbox_to_anchor=(1.05, 1), loc='upper left')

# TVジャンル別視聴時間のグラフ（2ndデータセット）
ax = axes[4, 1]
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)
bar_width = 0.8 / len(legend_categories)
for i, category in enumerate(legend_categories):
    category_color = category_color_dict[category]
    # 凡例用のバー（非表示）を追加
    ax.bar(0, 0, width=bar_width, color=category_color, label=category)
    # 実際のデータがある場合のみバーをプロット
    if category in category_duration_by_day_2nd.columns:
        ax.bar(category_duration_by_day_2nd['days'] + i * bar_width, category_duration_by_day_2nd[category], width=bar_width, color=category_color, align='edge')
ax.set_title(f'全ユーザー TVジャンル別 視聴時間（2ndデータセット）')
ax.set_ylabel('使用時間 (秒)')
ax.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')


# 左右のグラフのy軸の最大値を動的に計算する
for i in range(5):
    left_max = max(axes[i,0].get_ylim())
    right_max = max(axes[i,1].get_ylim())
    ymax = max(left_max, right_max) * 1.05
    axes[i,0].set_ylim(0, ymax)
    axes[i,1].set_ylim(0, ymax)


output_path = f'../data/img/all/Img_mix5_all_users_2rows_v2.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
plt.close()
print(f'Img_mix5_all_users_2rows_v2.png was output.')