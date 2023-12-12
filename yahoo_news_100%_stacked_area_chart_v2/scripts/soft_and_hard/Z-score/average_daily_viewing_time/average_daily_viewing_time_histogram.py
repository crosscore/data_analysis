import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import japanize_matplotlib

df = pd.read_csv('../../../../data/csv/soft_and_hard/device_add_days_viewing_time_del_outliers_iqr.csv', dtype={'user': str})

# Histogram settings
plt.figure(figsize=(10, 6))
plt.hist(df['viewing_time'], bins=200, color='skyblue', edgecolor='black')

# Set graph title and axis labels
plt.title('Distribution of viewing time')
plt.xlabel('Viewing time')
plt.ylabel('Frequency')

output_path = '../../../../data/img/soft_and_hard/iqr/viewing_time_distribution/histogram.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

plt.tight_layout()
plt.savefig(output_path)
plt.close()
print(f'{output_path} has been printed.')