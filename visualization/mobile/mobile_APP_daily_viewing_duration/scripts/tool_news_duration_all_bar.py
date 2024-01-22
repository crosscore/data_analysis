# tool_news_duration_all_bar.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import japanize_matplotlib
import os

data = pd.read_csv('./csv/APP_add_days.csv', dtype={'user': str})

output_dir = './img/tool_news/all/tool_news_bar'
os.makedirs(output_dir, exist_ok=True)

filtered_data = data[data['app_category'].isin(['ツール類', 'ニュース'])]

# 'days' と 'app_category' でグルーピングし、'duration' の合計を計算
grouped = filtered_data.groupby(['days', 'app_category'])['duration'].sum().reset_index()

# 全日付とカテゴリの組み合わせを作成する
all_combinations = pd.MultiIndex.from_product([range(1, 15), filtered_data['app_category'].unique()],
                                              names=['days', 'app_category']).to_frame(index=False)

# 組み合わせに対して、実データをマージし、存在しないデータには0を設定する
merged_data = all_combinations.merge(grouped, on=['days', 'app_category'], how='left').fillna(0)

# グラフのサイズを設定
plt.figure(figsize=(10, 6))

# Seabornを使って棒グラフをプロット
sns.barplot(x='days', y='duration', hue='app_category', data=merged_data, 
            palette='muted', dodge=True)  # dodge=Trueでカテゴリごとに別々の棒グラフを表示

plt.title('全ユーザーのツール類とニュースの使用時間')
plt.xlabel('日数')
plt.ylabel('合計使用時間（秒）')

# 凡例の位置を調整し、常に表示する
plt.legend(title='カテゴリ', loc='upper right')

plt.tight_layout()
plt.savefig(f'{output_dir}/all_users_usage.png', dpi=300)
plt.close()

print(f'画像 {output_dir}/all_users_usage.png を出力しました。')
