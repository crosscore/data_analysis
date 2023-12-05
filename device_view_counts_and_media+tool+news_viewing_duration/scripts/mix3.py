import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib as mpl
from matplotlib.font_manager import FontProperties

# Meiryoフォントのパスを指定
jp_font = FontProperties(fname='C:\\Windows\\Fonts\\meiryo.ttc')

device_data = pd.read_csv('./csv/device.csv', dtype={'user': str})
media_data = pd.read_csv('./csv/APP_media.csv', dtype={'user': str})

### Edit DF ###

# device_counts: device_dataから日毎のデバイス使用回数を集計
device_counts = device_data.groupby(['days', 'device_id']).size().unstack(fill_value=0).reindex(columns=[0, 1, 2, 3], fill_value=0).reset_index()

# media_dataからmediaとapp_categoryのデータを分けて集計
media_sum = media_data.groupby(['days', 'media'])['duration'].sum().unstack(fill_value=0).reindex(columns=['TV', 'PC', 'MB'], fill_value=0).reset_index()
app_cat_sum = media_data.groupby(['days', 'app_category'])['duration'].sum().unstack(fill_value=0).reindex(columns=['ツール類', 'ニュース'], fill_value=0).reset_index()

# 共通のdaysカラムを持つ新しいデータフレームを作成
common_days_df = pd.merge(device_counts[['days']], media_sum[['days']], on='days', how='outer')
common_days_df = pd.merge(common_days_df, app_cat_sum[['days']], on='days', how='outer').sort_values(by='days').reset_index(drop=True)

# device_counts, media_sum, app_cat_sumをcommon_days_dfとmergeして、全ての日に対する行を確保
device_counts = pd.merge(common_days_df[['days']], device_counts, on='days', how='left').fillna(0)
media_sum = pd.merge(common_days_df[['days']], media_sum, on='days', how='left').fillna(0)
app_cat_sum = pd.merge(common_days_df[['days']], app_cat_sum, on='days', how='left').fillna(0)


### グラフの作成 ###
sns.set(style="darkgrid")
fig, axes = plt.subplots(2, 1, figsize=(10, 10))

# 色の設定
device_colors = sns.color_palette("Set1", n_colors=4)
media_colors = sns.color_palette("Spectral", n_colors=6)
app_cat_colors = sns.color_palette("Blues", n_colors=2)

## deviceのグラフ ##
width = 0.2
x_labels = [f'Day {i}' for i in common_days_df['days']]  # Get day labels from the CSV file
for index, device_id in enumerate(device_counts.columns[1:]):
    axes[0].bar(np.arange(len(device_counts)) + index * width, device_counts[device_id], label=str(device_id),
                width=width, color=device_colors[index])

axes[0].set_xlabel('Days', fontproperties=jp_font)
axes[0].set_ylabel('View count (all users)', fontproperties=jp_font)
axes[0].legend(title='device_id', prop=jp_font)
axes[0].set_xticks(np.arange(len(common_days_df)))
axes[0].set_xticklabels(x_labels, fontproperties=jp_font)
axes[0].tick_params(axis='x', rotation=270)

## mediaとapp_categoryのグラフ ##
# mediaとapp_categoryの棒グラフを重ねるためのwidthを計算
total_width = 0.8
n_bars = 5  # TV, PC, MB, ツール類, ニュースの5本
bar_width = total_width / n_bars
x_indexes = np.arange(len(common_days_df))

# mediaの棒グラフ
for index, media in enumerate(media_sum.columns[1:]):
    axes[1].bar(x_indexes + index * bar_width, media_sum[media], label=media, width=bar_width,
                color=media_colors[index])

# app_categoryの棒グラフ
for index, app_cat in enumerate(app_cat_sum.columns[1:], start=3):  # mediaの棒グラフの次から開始
    axes[1].bar(x_indexes + index * bar_width, app_cat_sum[app_cat], label=app_cat, width=bar_width,
                color=app_cat_colors[index - 3])

axes[1].set_xlabel('Days', fontproperties=jp_font)
axes[1].set_ylabel('Total duration (seconds) (all users)', fontproperties=jp_font)
axes[1].legend(title='Category', prop=jp_font)
axes[1].set_xticks(x_indexes + total_width / 2 - bar_width / 2)  # X軸のラベル位置を中央に調整
axes[1].set_xticklabels(x_labels, fontproperties=jp_font)
axes[1].tick_params(axis='x', rotation=270)


### output ###
output_path = './img/total/Img_mix_total.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
print(f'Img_mix_total.png was output.')
plt.close()
