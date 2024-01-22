from scipy.stats import norm

# 仮のU値、期待値、標準偏差
U = 10  # 仮の観測されたU値
mu = 15  # U値の期待値
sigma = 5  # U値の標準偏差

# Zスコアの計算
Z = (U - mu) / sigma

# p値の計算
p_value = 2 * (1 - norm.cdf(abs(Z)))

print(f'p値: {p_value}')