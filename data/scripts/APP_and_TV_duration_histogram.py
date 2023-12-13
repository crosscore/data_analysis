import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
app_and_tv_before = pd.read_csv('../csv/mobile/original/TV_APP/TV_APP.csv', dtype={'user': str})
app_and_tv_after = pd.read_csv('../csv/mobile/original/TV_APP/IQR/TV_APP_apply_IQR.csv', dtype={'user': str})

app_iqr = pd.read_csv('../csv/mobile/original/TV_APP/IQR/APP_IQR.csv', dtype={'user': str})
tv_iqr = pd.read_csv('../csv/mobile/original/TV_APP/IQR/TV_IQR.csv', dtype={'user': str})

# draw histogram of df_before
plt.figure(figsize=(10, 6))
plt.hist(app_and_tv_before['duration'], bins=200, color='skyblue', edgecolor='black')
plt.title('Distribution of Viewing Time Before IQR')
plt.xlabel('Viewing Time')
plt.ylabel('Frequency')
plt.tight_layout()
output_path_before = '../img/mobile/TV_APP/histogram/iqr_before/histogram.png'
os.makedirs(os.path.dirname(output_path_before), exist_ok=True)
plt.savefig(output_path_before)
plt.close()
print(f'Image saved: {output_path_before}')

# draw histogram of df_after
plt.figure(figsize=(10, 6))
plt.hist(app_and_tv_after['duration'], bins=200, color='green', edgecolor='black')
plt.title('Distribution of Viewing Time After IQR')
plt.xlabel('Viewing Time')
plt.ylabel('Frequency')
plt.tight_layout()
output_path_after = '../img/mobile/TV_APP/histogram/iqr_after/histogram.png'
os.makedirs(os.path.dirname(output_path_after), exist_ok=True)
plt.savefig(output_path_after)
plt.close()
print(f'Image saved: {output_path_after}')

# draw histogram of app_iqr
plt.figure(figsize=(10, 6))
plt.hist(app_iqr['duration'], bins=200, color='green', edgecolor='black')
plt.title('Distribution of Viewing Time After IQR')
plt.xlabel('Viewing Time')
plt.ylabel('Frequency')
plt.tight_layout()
output_path_after = '../img/mobile/APP/histogram/iqr_after/histogram.png'
os.makedirs(os.path.dirname(output_path_after), exist_ok=True)
plt.savefig(output_path_after)
plt.close()
print(f'Image saved: {output_path_after}')

# draw histogram of tv_iqr
plt.figure(figsize=(10, 6))
plt.hist(tv_iqr['duration'], bins=200, color='green', edgecolor='black')
plt.title('Distribution of Viewing Time After IQR')
plt.xlabel('Viewing Time')
plt.ylabel('Frequency')
plt.tight_layout()
output_path_after = '../img/mobile/TV/histogram/iqr_after/histogram.png'
os.makedirs(os.path.dirname(output_path_after), exist_ok=True)
plt.savefig(output_path_after)
plt.close()
print(f'Image saved: {output_path_after}')