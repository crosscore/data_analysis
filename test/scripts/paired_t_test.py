import numpy as np
import scipy.stats as stats

exam1_scores = [63, 65, 56, 100, 88, 83, 77, 92, 90 ,84 ,68, 74, 87, 64, 71, 88]
exam2_scores = [69, 65, 62, 91, 78, 87, 79, 88, 85 ,92 ,69, 81, 84, 75, 84, 82]
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

#有意水準0.05のt分布の両側確率
alpha = 0.05
print(f'有意水準{alpha}のt分布の両側確率: {stats.t.interval(1 - alpha, df)}')