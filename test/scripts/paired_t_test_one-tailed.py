import numpy as np
import scipy.stats as stats

exam1_scores = [180, 130, 165, 155, 140]
exam2_scores = [150, 135, 145, 150, 140]
diff = np.array(exam1_scores) - np.array(exam2_scores)
print(f'exam1_scores: {exam1_scores}')
print(f'exam2_scores: {exam2_scores}')
print(f'差分: {diff}')
#差分の平均値
average_of_difference = np.mean(diff)
print(f'差分の平均値: {average_of_difference}')
#差分の分散
variance_of_difference = np.var(diff, ddof=1)
print(f'差分の分散: {variance_of_difference}')
#差分の標準偏差
std_of_difference = np.sqrt(variance_of_difference)
print(f'差分の標準偏差: {std_of_difference}')
#差分の標準誤差
se_of_difference = std_of_difference / np.sqrt(len(diff))
print(f'差分の標準誤差: {se_of_difference}')
#t値
t_value = average_of_difference / se_of_difference
print(f't値: {t_value}')
#自由度df
df = len(diff) - 1
print(f'自由度df: {df}')
#有意水準0.05のt分布の片側確率
alpha = 0.05
print(f'有意水準{alpha}のt分布の片側確率: {stats.t.interval(1 - alpha, df)}')
#exam1_scoresとexam2_scoresにおいて、対応のあるt検定(片側検定)を行う
print('================================================')
print('exam1_scoresとexam2_scoresにおいて、対応のあるt検定(片側検定)を行う')
t, p = stats.ttest_rel(exam1_scores, exam2_scores)

#片側検定のためp値を2で割る
p_one_side = p / 2

if t < 0:
    p_one_side = 1 - p_one_side

print(f't値: {t}')
print(f'p値: {p_one_side}')
print(f'{p_one_side} < {alpha} : 有意差あり' if p_one_side < alpha else f'{p_one_side} > {alpha} : 有意差なし')