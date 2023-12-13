#yahoo_news_100%_stacked_area_chart_user.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

df = pd.read_csv('../../../../data/csv/soft_and_hard/iqr/device_add_days_viewing_time_del_outliers_soft_hard.csv', dtype={'user': str})
#category_list = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT', '科学', 'ライフ', '地域']
category_list = ['soft_news', 'hard_news']

# Create a figure with a 3x5 grid of subplots
fig, axes = plt.subplots(5, 3, figsize=(15, 25)) # Adjust the figsize as needed
axes = axes.flatten() # Flatten the axes array for easy indexing

users = df['user'].unique()

# Iterate over each user and plot in the respective subplot
for i, user in enumerate(users):
    user_df = df[df['user'] == user]
    category_totals = user_df.groupby(['days', 'category'])['viewing_time'].sum().unstack(fill_value=0).reindex(columns=category_list, fill_value=0)
    days_range = np.arange(1, 15)
    category_totals = category_totals.reindex(days_range, fill_value=0) # Set date range
    category_percentage = category_totals.div(category_totals.sum(axis=1), axis=0)

    # Plot settings for each user
    category_colors = sns.color_palette("hls", n_colors=len(category_list))
    category_percentage.plot(kind='area', stacked=True, color=category_colors, ax=axes[i])
    axes[i].set_title(f'User {user}')
    axes[i].set_xlabel('Days')
    axes[i].set_ylabel('Percentage')

    # Set x-axis ticks and labels
    x_ticks = days_range
    x_labels = [f'Day {i}' for i in x_ticks]
    axes[i].set_xticks(x_ticks)
    axes[i].set_xticklabels(x_labels, rotation=45)

    # Set x-axis range
    axes[i].set_xlim(days_range[0], days_range[-1])

    # Set legend for the first subplot only
    if i == 0:
        handles, labels = axes[i].get_legend_handles_labels()
        fig.legend(handles, labels, title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout
plt.tight_layout()

# Output path for the combined PNG file
output_path = f'../../../../data/img/soft_and_hard/iqr_one_img/analysis_by_total_viewing_time/100%_stacked_area_chart/user/combined_users_stacked_area_chart.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the figure
plt.savefig(output_path)
plt.close()

print(f'{output_path} output completed.')
