import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

df = pd.read_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time.csv', dtype={'user': str})

# Histogram settings
plt.figure(figsize=(10, 6))
plt.hist(df['viewing_time'], bins=50, color='skyblue', edgecolor='black')

# Set graph title and axis labels
plt.title('Distribution of viewing time')
plt.xlabel('Viewing time')
plt.ylabel('Frequency')

output_path = '../../data/img/Raw/histogram.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

plt.tight_layout()
plt.savefig(output_path)
plt.close()
print(f'{output_path} has been printed.')


df = pd.read_csv('../../data/csv/remove_outliers/device_add_days_viewing_time_del_outliers_iqr.csv', dtype={'user': str})

# Histogram settings
plt.figure(figsize=(10, 6))
plt.hist(df['viewing_time'], bins=50, color='skyblue', edgecolor='black')

# Set graph title and axis labels
plt.title('Distribution of viewing time')
plt.xlabel('Viewing time')
plt.ylabel('Frequency')

output_path = '../../data/img/IQR/histogram.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

plt.tight_layout()
plt.savefig(output_path)
plt.close()
print(f'{output_path} has been printed.')