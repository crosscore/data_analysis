import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

df = pd.read_csv('../../../../data/csv/soft_and_hard/iqr/device_add_days_viewing_time_del_outliers_soft_hard.csv', dtype={'user': str})

# Create a figure with a 3x5 grid of subplots
fig, axes = plt.subplots(5, 3, figsize=(15, 25)) # Adjust the figsize as needed
axes = axes.flatten() # Flatten the axes array for easy indexing

# Iterate over each user and plot in the respective subplot
for i, user in enumerate(df['user'].unique()[:15]): # Limit to first 15 users
    user_df = df[df['user'] == user]
    average_viewing_time = user_df.groupby('days')['viewing_time'].mean()

    # Plot settings for each user
    average_viewing_time.plot(kind='bar', color='skyblue', ax=axes[i])
    axes[i].set_title(f'User {user}')
    axes[i].set_xlabel('Days')
    axes[i].set_ylabel('Average Viewing Time')

# Adjust layout
plt.tight_layout()

# Output path for the combined PNG file
output_path = '../../../../data/img/soft_and_hard/iqr_one_img/average_viewing_time_by_day/user/bar_chart_user.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

plt.savefig(output_path)
plt.close()

print(f'{output_path} output completed.')
