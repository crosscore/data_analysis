import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import japanize_matplotlib

# Z値の範囲を設定
z_values = np.linspace(-4, 4, 1000)

# 標準正規分布の確率密度関数 (PDF) と累積分布関数 (CDF)
pdf_values = norm.pdf(z_values)
cdf_values = norm.cdf(z_values)

# PDFとCDFのプロット
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(z_values, pdf_values, label='PDF')
plt.title('標準正規分布 (PDF)')
plt.xlabel('Z値')
plt.ylabel('確率密度')
plt.grid(True)

plt.subplot(1, 2, 2)
plt.plot(z_values, cdf_values, label='CDF', color='red')
plt.title('累積分布関数 (CDF)')
plt.xlabel('Z値')
plt.ylabel('累積確率')
plt.grid(True)

plt.tight_layout()
plt.savefig('pdf_and_cdf.png', dpi=300)
