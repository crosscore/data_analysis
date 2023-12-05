#mix_days_user.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

device_data = pd.read_csv('./filtered_csv/filtered_device.csv', dtype={'user': str})
media_data = pd.read_csv('./filtered_csv/filtered_media.csv', dtype={'user': str})

user_list = device_data['user'].unique()

for user in user_list:
    user_device_data = device_data[device_data['user'] == user].copy()
    user_media_data = media_data[media_data['user'] == user].copy()

    #.reindex(): 指定された列名のリストに基づいてDFの列を再インデックス。指定された列名の順序を保証。
    device_counts = user_device_data.groupby(['days', 'device_id']).size().unstack(fill_value=0).reindex(columns=[0, 1, 2, 3], fill_value=0).reset_index()
    media_sum = user_media_data.groupby(['days', 'media'])['viewing_duration'].sum().unstack(fill_value=0).reindex(columns=['TV', 'PC', 'MB'], fill_value=0).reset_index()

    # 共通のdaysカラムを持つcommon_days_dfを作成
    common_days_df = pd.merge(device_counts[['days']], media_sum[['days']], on='days', how='outer')
    #reset_index():DFのindexをデフォルト整数にreset
    common_days_df = common_days_df.sort_values(by='days').reset_index(drop=True)

    # device_countsとcommon_days_dfとマージして、全ての日に対する行を確保する
    device_counts = pd.merge(common_days_df[['days']], device_counts, on='days', how='left').fillna(0)
    media_sum = pd.merge(common_days_df[['days']], media_sum, on='days', how='left').fillna(0)


    sns.set(style="darkgrid")
    # 2行1列のサブプットを作成し、そのサイズを10x10に設定 (fig:図オブジェクト, axes:軸オブジェクト)
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    device_colors = sns.color_palette("Set1", n_colors=4)
    media_colors = sns.color_palette("Set2", n_colors=3)

    ## deviceのグラフ ##
    width = 0.2
    x_labels = [f'Day {i}' for i in common_days_df['days']]  # x_labels: ['Day 1', 'Day 2', ..., 'Day 14']
    for index, device_id in enumerate(device_counts.columns[1:]): #device_counts(DF)の1列目からループ
        axes[0].bar(np.arange(len(device_counts)) + index * width, device_counts[device_id], label=str(device_id),
                    width=width, color=device_colors[index]) # axes[0]に棒グラフを追加。device_id毎に異なる色を使用。X軸の位置はindex * widthでオフセット
    axes[0].set_xlabel('Days')
    axes[0].set_ylabel(f'View count (user {user})')
    axes[0].legend(title='device_id')
    axes[0].set_xticks(np.arange(len(common_days_df))) #np.arrange(len(common_days_df)): [0, 1, 2, ..., 9]。この場合tickはx軸の整数位置に配置
    axes[0].set_xticklabels(x_labels)
    axes[0].tick_params(axis='x', rotation=270)

    ## mediaのグラフ ##
    width = 0.2666
    for index, media in enumerate(media_sum.columns[1:]):
        axes[1].bar(np.arange(len(media_sum)) + index * width, media_sum[media], label=media, width=width,
                    color=media_colors[index])
    axes[1].set_xlabel('Days')
    axes[1].set_ylabel(f'Total viewing time (seconds) (user {user})')
    axes[1].legend(title='media')
    axes[1].set_xticks(np.arange(len(common_days_df)))
    axes[1].set_xticklabels(x_labels)
    axes[1].tick_params(axis='x', rotation=270)

    output_path = f'./img/user/Img_mix_{user}.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'Img_mix_{user}.png was output.')