import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_user_category_duration(df, file_name):
    fig, axes = plt.subplots(5, 3, figsize=(15, 25)) # Adjust the figsize as needed
    axes = axes.flatten() # Flatten the axes array for easy indexing

    users = df['user'].unique()[:15] # Limit to first 15 users

    # Iterate over each user and plot in the respective subplot
    for i, user in enumerate(users):
        user_df = df[df['user'] == user]
        category_totals = user_df.groupby(['days', 'category'])['duration'].sum().unstack(fill_value=0)
        days_range = np.arange(1, 15)
        category_totals = category_totals.reindex(days_range, fill_value=0) # Ensure all days are included

        # Plot settings for each user
        category_totals.plot(kind='bar', stacked=True, color=sns.color_palette("hls", n_colors=len(category_totals.columns)), ax=axes[i])
        axes[i].set_title(f'User {user}')
        axes[i].set_xlabel('Days')
        axes[i].set_ylabel('Total Duration')

        # Set x-axis ticks and labels
        x_ticks = np.arange(len(days_range))
        x_labels = [f'Day {day}' for day in days_range]
        axes[i].set_xticks(x_ticks)
        axes[i].set_xticklabels(x_labels, rotation=45)

        # Set x-axis range
        axes[i].set_xlim(-0.5, len(days_range) - 0.5)  # Set x-axis range to include all bars

        # Set legend for the first subplot only
        if i == 0:
            handles, labels = axes[i].get_legend_handles_labels()
            fig.legend(handles, labels, title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust layout
    plt.tight_layout()

    # Output path for the combined PNG file
    output_path = f'../../../data/img/soft_and_hard/total_duration/bar_chart/user/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the figure
    plt.savefig(output_path)
    plt.close()

    print(f'{output_path} output completed.')

# Load datasets
df_app = pd.read_csv('../../../data/csv/soft_and_hard/APP.csv', dtype={'user': str})
df_tv = pd.read_csv('../../../data/csv/soft_and_hard/TV.csv', dtype={'user': str})

# Plot and save category duration for each user in each dataset
plot_user_category_duration(df_app, 'app_total_duration_user.png')
plot_user_category_duration(df_tv, 'tv_total_duration_user.png')
