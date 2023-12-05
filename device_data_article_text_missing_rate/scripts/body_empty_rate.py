import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#本文が空のデータの存在率のグラフを生成する

data = pd.read_csv('../data/csv/combine_csv/all_user_plus_json.csv', dtype={'user': str})
# userごとのbodyの欠損数を計算
body_empty_counts = data.groupby('user')['body'].apply(lambda x: x.isnull().sum())
# userごとのデータの数を計算
total_counts = data.groupby('user').size()
# bodyの欠損率を計算
body_empty_ratio = (body_empty_counts / total_counts) * 100

sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(10, 6))
# bodyの欠損率を示す棒グラフの作成
sns.barplot(x=body_empty_ratio.index, y=body_empty_ratio.values, ax=ax)
ax.set_xlabel('User ID')
ax.set_ylabel('Body Empty Ratio (%)')
ax.set_ylim(0, 100)  

output_path = f'../data/img/user_body_empty_ratio.png'
print(f'user_body_empty_ratio.png was output.')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
plt.close()
