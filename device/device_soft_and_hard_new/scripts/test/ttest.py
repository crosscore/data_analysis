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



# LaTeX数式の設定
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# LaTeX数式
mannwhitneyu_text = """
検定統計量 $U$ の計算に必要な数値を用意する。\n
[1] 標本サイズ $n_{\\mathrm{A}} \\quad n_{\\mathrm{B}}$\n
[2] 順位和 $R_{\\mathrm{A}} \\quad R_{\\mathrm{B}}$\n
STEP 2\n
検定統計量 $U$ の候補として、 $U_1$ と $U_2$ を計算する。\n
$$\n
U_1=n_{\\mathrm{A}} n_{\\mathrm{B}}+\\frac{1}{2} n_{\\mathrm{A}}\\left(n_{\\mathrm{A}}+1\\right)-R_{\\mathrm{A}}\n
$$\n
$$\n
U_2=n_{\\mathrm{A}} n_{\\mathrm{B}}+\\frac{1}{2} n_{\\mathrm{B}}\\left(n_{\\mathrm{B}}+1\\right)-R_{\\mathrm{B}}\n
$$\n
$U_1$ と $U_2$ のうち、より小さな値を $U$ とする。\n
計算して得た $U$ と臨界値 $U_{0.05}$ の間に以下の不等式が成立するとき\n
$$\n
U \\leq U_{0.05}\n
$$\n
「統計的に有意な差が認められた $(P<0.05)$ と結論する。\n
この不等式が満たされなければ「統計的に有意な差は認められなかった」と結論する。\n
"""

# 図の生成
fig, ax = plt.subplots(figsize=(8, 10))
ax.text(0.5, 0.5, mannwhitneyu_text, fontsize=12, ha='center', va='center', wrap=True)
ax.axis('off')
plt.savefig('mannwhitneyu_formula_jp.png')
