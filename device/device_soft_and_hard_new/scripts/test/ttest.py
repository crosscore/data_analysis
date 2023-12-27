from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import scipy.stats as stats
import japanize_matplotlib

def draw_text(text, position, fontsize=12, color='black', ax=None):
    if ax is None:
        ax = plt
    ax.text(position[0], position[1], text, fontsize=fontsize, color=color, ha='center')

# 自由度を選択
df = 10

# t値の範囲を設定
t_values = np.linspace(-4, 4, 100)

# t分布の確率密度関数 (PDF) を計算
pdf_values = stats.t.pdf(t_values, df)

fig, axs = plt.subplots(2, 1, figsize=(10, 14))

ax = axs[0]
ax.axis('off')
draw_text(r'$\bar{x}_1, \bar{x}_2$ : グループ1, 2の平均値', (0.5, 0.95), ax=ax)
draw_text(r'$\Delta \bar{x} = \bar{x}_1 - \bar{x}_2$ : 平均値の差', (0.5, 0.9), ax=ax)
draw_text(r'$s_1, s_2$ : グループ1, 2の標準偏差', (0.5, 0.85), ax=ax)
draw_text(r'$n_1, n_2$ : グループ1, 2のサンプルサイズ', (0.5, 0.8), ax=ax)
draw_text(r'$SE = \sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}$ : 標準誤差', (0.5, 0.75), ax=ax)
draw_text(r'$t = \frac{\Delta \bar{x}}{SE}$ : t値', (0.5, 0.7), ax=ax)
draw_text(r'$df = n_1 + n_2 - 2$ : 自由度', (0.5, 0.65), ax=ax)
draw_text('t分布表を用いてp値を求める', (0.5, 0.6), ax=ax)
draw_text('片側検定：その確率がp値', (0.5, 0.55), ax=ax)
draw_text('両側検定：その確率を2倍した値がp値', (0.5, 0.5), ax=ax)
draw_text('t分布表とは', (0.5, 0.45), ax=ax)
draw_text('特定の自由度におけるt値の確率分布を示す表。', (0.5, 0.4), ax=ax)
draw_text('帰無仮説が真である場合に、そのt値（またはそれ以上の極端な値）が得られる確率を表す。', (0.5, 0.35), ax=ax)
draw_text('表から得られる確率（p値）を用いて、結果の統計的有意性を判断する。', (0.5, 0.3), ax=ax)

ax = axs[1]
ax.plot(t_values, pdf_values, label=f'DF = {df}')
ax.fill_between(t_values, pdf_values, 0, alpha=0.2)
ax.set_title('t分布のグラフ (自由度 = 10)')
ax.set_xlabel('t値')
ax.set_ylabel('確率密度')
ax.legend()

plt.tight_layout()
plt.savefig('t_test_formula_and_t_dist_table_with_graph_jp.png')


fig, ax = plt.subplots(figsize=(10, 24))
ax.axis('off')

# Mann-Whitney U検定の計算式
mannwhitneyu_text = [
    r'$U_1 = R_1 - \frac{n_1(n_1+1)}{2}$ : グループ1のU値',
    r'$U_2 = R_2 - \frac{n_2(n_2+1)}{2}$ : グループ2のU値',
    r'$R_1, R_2$ : グループ1, 2のデータにランクをつけた合計',
    r'$n_1, n_2$ : グループ1, 2のサンプルサイズ',
    r'ランク付け: 全データを合わせて小さい順にランク付け',
    r'同じ値がある場合は、その値の平均ランクを割り当てる',
    r'使用するU値は、$U_1$ と $U_2$ の小さい方',
    r'帰無仮説: 二つのサンプルが同じ母集団から来ている',
    r'対立仮説: 二つのサンプルが異なる母集団から来ている',
    r'p値の計算には正規近似または厳密法を使用',
    r'p値 < 有意水準 ⇒ 帰無仮説を棄却、統計的に有意な差がある',
    '',
    'ランク付けの例:',
    'データ: グループ1 [3, 1, 2], グループ2 [5, 6, 4]',
    '合算して並べる: [1, 2, 3, 4, 5, 6]',
    'ランク付け: [1, 2, 3, 4, 5, 6]',
    'グループ1のランク合計: $R_1 = 1 + 2 + 3 = 6$',
    'グループ2のランク合計: $R_2 = 4 + 5 + 6 = 15$',
    '',
    'p値の計算:',
    '小さなサンプルサイズでは厳密法を使用',
    '大きなサンプルサイズでは正規近似を使用',
    '厳密法: 全ての可能なランクの組み合わせを考慮',
    '正規近似: U値を標準正規分布に変換してp値を求める',

    r'正規近似によるp値の計算:',
    r'U値の期待値: $\mu = \frac{n_1 n_2}{2}$',
    r'U値の分散: $\sigma^2 = \frac{n_1 n_2 (n_1 + n_2 + 1)}{12}$',
    r'標準化されたZスコア: $Z = \frac{U - \mu}{\sigma}$',
    r'Zスコアに基づいてp値を求める: $p = 2 \times (1 - \text{CDF}(Z))$',
    r'p値が有意水準より小さい場合、統計的に有意な差があると判断'
]

# テキストをプロット
for i, text in enumerate(mannwhitneyu_text):
    draw_text(text, (0.5, 1 - i*0.05), ax=ax)

plt.title("Mann-Whitney U検定の計算式とランクの説明", fontsize=16, pad=20)
file_path = 'mannwhitneyu_formula_and_rank_explanation.png'
plt.savefig(file_path, bbox_inches='tight')
