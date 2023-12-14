#mix_days_total.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

device_data = pd.read_csv('./filtered_csv/filtered_device.csv', dtype={'user': str})
media_data = pd.read_csv('./filtered_csv/filtered_media.csv', dtype={'user': str})

# device_counts, media_sum: それぞれのDFから日毎のデバイス使用回数とメディア視聴時間を集計
device_counts = device_data.groupby(['days', 'device_id']).size().unstack(fill_value=0).reindex(columns=[0, 1, 2, 3], fill_value=0).reset_index()
media_sum = media_data.groupby(['days', 'media'])['duration'].sum().unstack(fill_value=0).reindex(columns=['TV', 'PC', 'MB'], fill_value=0).reset_index()

# 共通のdaysカラムを持つ新しいデータフレームを作成
common_days_df = pd.merge(device_counts[['days']], media_sum[['days']], on='days', how='outer') #how='outer':外部結合:両方のDFの全ての値を含む結果を生成。
common_days_df = common_days_df.sort_values(by='days').reset_index(drop=True) #drop=True:既存のindex列を新しい列として保持せずに削除。
print(common_days_df)

# device_countsとmedia_sumをcommon_days_dfとmergeして、全ての日に対する行を確保する
device_counts = pd.merge(common_days_df[['days']], device_counts, on='days', how='left').fillna(0)
media_sum = pd.merge(common_days_df[['days']], media_sum, on='days', how='left').fillna(0)


sns.set(style="darkgrid")
fig, axes = plt.subplots(2, 1, figsize=(10, 10))
device_colors = sns.color_palette("Set1", n_colors=4)
media_colors = sns.color_palette("Set2", n_colors=3)

## deviceのグラフ ##
width = 0.2
x_labels = [f'Day {i}' for i in common_days_df['days']]  # Get day labels from the CSV file
print(x_labels)
for index, device_id in enumerate(device_counts.columns[1:]):
    axes[0].bar(np.arange(len(device_counts)) + index * width, device_counts[device_id], label=str(device_id),
                width=width, color=device_colors[index])
axes[0].set_xlabel('Days')
axes[0].set_ylabel(f'View count (all users)')
axes[0].legend(title='device_id') #凡例表示
axes[0].set_xticks(np.arange(len(common_days_df)))
axes[0].set_xticklabels(x_labels)
axes[0].tick_params(axis='x', rotation=270)

## mediaのグラフ ##
width = 0.2666
for index, media in enumerate(media_sum.columns[1:]):
    axes[1].bar(np.arange(len(media_sum)) + index * width, media_sum[media], label=media, width=width,
                color=media_colors[index])
axes[1].set_xlabel('Days')
axes[1].set_ylabel(f'Total viewing time (seconds) (all users)')
axes[1].legend(title='media')
axes[1].set_xticks(np.arange(len(common_days_df)))
axes[1].set_xticklabels(x_labels)
axes[1].tick_params(axis='x', rotation=270)


output_path = f'./img/total/Img_mix_total.png'
print(f'Img_mix_total.png was output.')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
plt.close()
