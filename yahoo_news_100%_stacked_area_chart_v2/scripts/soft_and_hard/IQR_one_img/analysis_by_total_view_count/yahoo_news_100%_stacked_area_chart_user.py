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

# Flatten the axes array for easy indexing
axes = axes.flatten()

for i, user in enumerate(df['user'].unique()[:15]): # Limit to first 15 users
    user_df = df[df['user'] == user]
    # Process data
    category_totals = user_df.groupby(['days', 'category']).size().unstack(fill_value=0).reindex(columns=category_list, fill_value=0)

    # Ensure date range
    days_range = np.arange(1, 15)
    category_totals = category_totals.reindex(days_range, fill_value=0) # Set date range

    # Calculate the percentage of each category
    category_percentage = category_totals.div(category_totals.sum(axis=1), axis=0)

    # Plot settings
    x_ticks = days_range
    x_labels = [f'Day {i}' for i in x_ticks]

    # Create a 100% stacked area chart in the subplot
    category_colors = sns.color_palette("hls", n_colors=len(category_list))
    category_percentage.plot(kind='area', stacked=True, color=category_colors, ax=axes[i])

    # Subplot title and labels
    axes[i].set_title(f'User {user}')
    axes[i].set_ylabel('Percentage')
    axes[i].set_xlabel('Days')

    # Set x-axis ticks and labels
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
output_path = '../../../../data/img/soft_and_hard/iqr_one_img/analysis_by_total_view_count/100%_stacked_area_chart/combined_users_stacked_area_chart.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Save the figure
plt.savefig(output_path)
plt.close()

print(f'{output_path} was output.')
