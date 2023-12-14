import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import japanize_matplotlib
import os

data = pd.read_csv('./APP_add_days_del_user.csv', dtype={'user': str})

# 各ユーザー、日付、およびアプリごとにdurationを合計
duration_per_user_per_day_per_app = data.groupby(['user', 'days', 'app_name']).sum()['duration'].reset_index()

# 各ユーザー、日付ごとにアプリごとのdurationをpivotすることで、アプリごとの列を作成
pivot_data = duration_per_user_per_day_per_app.pivot_table(
    index=['user', 'days'],
    columns='app_name',
    values='duration',
    fill_value=0
)

# ユーザーごとにデータを分割
for user, user_data in pivot_data.groupby(level=0):
    # 総使用時間でアプリを並べ替え
    app_order = user_data.sum().sort_values(ascending=False).index
    user_data = user_data[app_order]  # 並べ替えた順序で列を並べ替え

    # カラーマップの選択と範囲の調整
    colors = plt.cm.viridis_r(np.linspace(0, 20, len(user_data.columns)))  # viridis_rカラーマップを設定

    # 積み上げバープロットを作成
    fig, ax = plt.subplots(figsize=(12, 8))
    user_data.index = user_data.index.droplevel(0)  # Remove the user level from the index
    user_data.plot(kind='bar', stacked=True, ax=ax, color=colors)  # グラデーションカラーを適用
    ax.set_title(f'Total duration of app usage for user {user} per day')
    ax.set_ylabel('Total Duration (seconds)')
    ax.set_xlabel('Day')
    ax.legend().set_visible(False)  # Hide legend on the graph plot
    
    # グラフを保存
    graph_output_path = f'./img/graph_app_user_days_app_duration_sort/user/Img_graph_app_user_{user}_days_app_duration.png'
    os.makedirs(os.path.dirname(graph_output_path), exist_ok=True)  # Create directory if it doesn't exist
    fig.savefig(graph_output_path)
    
    # 凡例を作成し保存
    fig_leg = plt.figure(figsize=(5, 5))
    ax_leg = fig_leg.add_subplot(111)
    # 凡例にはユーザーが使用したアプリのみを表示
    used_apps = user_data.columns[user_data.sum() > 0]
    handles, labels = ax.get_legend_handles_labels()
    # ソートする前に used_handles と used_labels を定義
    used_handles, used_labels = zip(*[(handle, label) for handle, label in zip(handles, labels) if label in used_apps])
    # 凡例を総使用時間で並べ替え
    used_handles_labels = sorted(zip(used_handles, used_labels), key=lambda x: list(app_order).index(x[1]), reverse=False)
    used_handles, used_labels = zip(*used_handles_labels)
    ax_leg.legend(used_handles, used_labels, loc='center')
    ax_leg.axis('off')
    legend_output_path = f'./img/graph_app_user_days_app_duration_sort/user/Img_legend_app_user_{user}.png'
    fig_leg.savefig(legend_output_path, bbox_inches='tight')
    
    plt.close(fig)
    plt.close(fig_leg)