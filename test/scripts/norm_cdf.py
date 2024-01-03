from scipy.stats import norm

probability = norm.cdf(2) - norm.cdf(-2)
print(probability)

# αの値を設定（例：0.05）
alpha = 0.025

# 上側100α％点を計算（norm.ppfは累積分布関数の逆関数）
upper_percentile = norm.ppf(1 - alpha)
print(upper_percentile)

z_score = 1.64
# zスコア1.64以上の値を取る確率を計算
probability_above_correct_z = norm.sf(z_score)
print(probability_above_correct_z)
