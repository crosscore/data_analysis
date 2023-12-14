import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_percentage_category_duration(df, file_name):
    # Get unique categories dynamically
    categories = df['category'].unique()

    # Process data
    category_totals = df.groupby(['days', 'category']).size().unstack(fill_value=0)
    days_range = np.arange(1, 15)
    category_totals = category_totals.reindex(days_range, fill_value=0)

    # Calculate the percentage of each category
    category_percentage = category_totals.div(category_totals.sum(axis=1), axis=0)

    # Plot settings
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    category_colors = sns.color_palette("hls", n_colors=len(categories))
    category_percentage.plot(kind='area', stacked=True, color=category_colors, ax=ax)

    # Set titles and labels
    ax.set_title('Percentage of Views for All Users')
    ax.set_ylabel('Percentage')
    ax.set_xlabel('Days')

    # Set x-axis ticks and labels
    x_ticks = days_range
    x_labels = [f'Day {i}' for i in x_ticks]
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=45)

    # Set x-axis range
    ax.set_xlim(days_range[0], days_range[-1])

    # Set legend
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, categories, title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Save the figure
    output_path = f'../../../data/img/soft_and_hard/view_counts/100%_stacked_area_chart/all/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} was output.')

# Load datasets
df_app = pd.read_csv('../../../data/csv/soft_and_hard/APP.csv', dtype={'user': str})
df_tv = pd.read_csv('../../../data/csv/soft_and_hard/TV.csv', dtype={'user': str})

# Plot and save the graph for each dataset
plot_percentage_category_duration(df_app, 'app_100%_stacked_area_chart_view_counts.png')
plot_percentage_category_duration(df_tv, 'tv_100%_stacked_area_chart_view_counts.png')
