import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

#本文が存在する割合のグラフを作成

data = pd.read_csv('../data/csv/combine_csv/all_user_plus_json.csv', dtype={'user': str})
# userごとのbodyの存在する数を計算
body_non_empty_counts = data.groupby('user')['body'].apply(lambda x: x.notnull().sum())
# userごとのデータの数を計算
total_counts = data.groupby('user').size()
# bodyの存在率を計算
body_exist_ratio = (body_non_empty_counts / total_counts) * 100

sns.set(style="darkgrid")
fig, ax = plt.subplots(figsize=(10, 6))
# bodyの存在率を示す棒グラフの作成
sns.barplot(x=body_exist_ratio.index, y=body_exist_ratio.values, ax=ax)
ax.set_xlabel('User ID')
ax.set_ylabel('Body Exist Ratio (%)')
ax.set_ylim(0, 100)  

output_path = f'../data/img/user_body_exist_ratio.png'
print(f'user_body_exist_ratio.png was output.')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
plt.close()
