#days_app_and_media_total.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

device_data = pd.read_csv('./filtered_csv/filtered_device.csv', dtype={'user': str})
app_data = pd.read_csv('./filtered_all_csv/media_news_csv/concat_csv/APP_concat_media.csv', dtype={'user': str})

# 特定のapp_categoryとmediaのデータをフィルタリング
filtered_app_data = app_data[
    (app_data['app_category'].isin(['ツール類', 'ニュース'])) | 
    (app_data['media'].isin(['PC', 'TV', 'MB']))
]

# 日毎にdurationの合計を計算
app_category_sum = filtered_app_data[filtered_app_data['app_category'].isin(['ツール類', 'ニュース'])].groupby(['days', 'app_category'])['duration'].sum().unstack(fill_value=0)
media_sum = filtered_app_data[filtered_app_data['media'].isin(['PC', 'TV', 'MB'])].groupby(['days', 'media'])['duration'].sum().unstack(fill_value=0)
print(app_category_sum)

# deviceの使用回数を日毎に集計
device_counts = device_data.groupby(['days', 'device_id']).size().unstack(fill_value=0)

# インデックスとなっている 'days' をカラムに変換
device_counts.reset_index(inplace=True)
app_category_sum.reset_index(inplace=True)
media_sum.reset_index(inplace=True)

# 'days' カラムを文字列型に変換する
device_counts['days'] = device_counts['days'].astype(str)
app_category_sum['days'] = app_category_sum['days'].astype(str)
media_sum['days'] = media_sum['days'].astype(str)

# 共通のdaysカラムを持つ新しいデータフレームを作成し、device_countsとapp_category_sum、media_sumをマージ
common_days_df = pd.DataFrame({'days': pd.date_range(start=device_data['date'].min(), end=device_data['date'].max()).strftime('%Y-%m-%d')})
device_counts = common_days_df.merge(device_counts, on='days', how='left').fillna(0)
app_category_sum = common_days_df.merge(app_category_sum, on='days', how='left').fillna(0)
media_sum = common_days_df.merge(media_sum, on='days', how='left').fillna(0)


sns.set(style="darkgrid")
fig, axes = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

device_colors = sns.color_palette("Set1", n_colors=device_counts.shape[1])
device_width = 0.15
x = np.arange(len(common_days_df))
for index, (column, color) in enumerate(zip(device_counts.columns[1:], device_colors)):
    axes[0].bar(x + index * device_width, device_counts[column], width=device_width, label=str(column), color=color)
axes[0].set_title('Device Usage Count by Day')
axes[0].set_ylabel('Usage Count')
axes[0].set_xticks(x + device_width)
axes[0].set_xticklabels(common_days_df['days'], rotation=45)
axes[0].legend(title='Device ID')

app_media_colors = sns.color_palette("Set2", n_colors=5)
app_media_width = 0.1
app_media_categories = app_category_sum.columns.tolist() + media_sum.columns.tolist()
for index, (column, color) in enumerate(zip(app_media_categories, app_media_colors)):
    # appのデータをプロット
    if column in app_category_sum.columns:
        axes[1].bar(x + index * app_media_width, app_category_sum[column], width=app_media_width, label=column, color=color)
    # mediaのデータをプロット
    elif column in media_sum.columns:
        axes[1].bar(x + index * app_media_width, media_sum[column], width=app_media_width, label=column, color=color)
axes[1].set_title('App Duration and Media Viewing Time by Category and Day')
axes[1].set_xlabel('Days')
axes[1].set_ylabel('Total Duration (seconds)')
axes[1].set_xticks(x + app_media_width)
axes[1].set_xticklabels(common_days_df['days'], rotation=45)
axes[1].legend(title='App Category / Media')

plt.tight_layout()
output_path = './img/total/Img_device_media_total.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path)
plt.close()
print(f'Img_device_media_total.png was output.')
