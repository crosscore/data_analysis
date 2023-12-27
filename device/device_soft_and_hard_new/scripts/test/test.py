# 必要なライブラリをインポート
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# シード値を設定して再現性を確保
np.random.seed(0)

# サンプルデータを生成
# グループA: 平均50、標準偏差5の正規分布から100個のデータを生成
# グループB: 平均50.5、標準偏差5の正規分布から100個のデータを生成
# グループC: 平均55、標準偏差20の正規分布から100個のデータを生成（平均に差があるが分散が大きい）
group_A = np.random.normal(50, 5, 100)
group_B = np.random.normal(50.5, 5, 100)
group_C = np.random.normal(56, 20, 100)

# グループAとグループBのt検定
stat_AB, p_value_AB = stats.ttest_ind(group_A, group_B)
# グループAとグループCのt検定
stat_AC, p_value_AC = stats.ttest_ind(group_A, group_C)

# p値が5%未満かどうかを確認
significant_AB = p_value_AB < 0.05
significant_AC = p_value_AC < 0.05

# プロットの作成
plt.figure(figsize=(15, 5))

# グループAとBのヒストグラム
plt.subplot(1, 2, 1)
plt.hist(group_A, bins=20, alpha=0.7, label='Group A')
plt.hist(group_B, bins=20, alpha=0.7, label='Group B')
plt.title(f'Group A vs Group B\np-value: {p_value_AB:.4f} - {"Significant" if significant_AB else "Not Significant"}')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()

# グループAとCのヒストグラム
plt.subplot(1, 2, 2)
plt.hist(group_A, bins=20, alpha=0.7, label='Group A')
plt.hist(group_C, bins=20, alpha=0.7, label='Group C')
plt.title(f'Group A vs Group C\np-value: {p_value_AC:.4f} - {"Significant" if significant_AC else "Not Significant"}')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.legend()

# プロットを表示
plt.tight_layout()
plt.savefig('t-test.png')

# p値の結果を出力
p_value_AB, p_value_AC, significant_AB, significant_AC
