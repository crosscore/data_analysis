import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_total_category_percentage(df, file_name):
    category_list = ['soft', 'hard']
    category_totals = df.groupby(['days', 'category'])['duration'].sum().unstack(fill_value=0).reindex(columns=category_list, fill_value=0)
    days_range = np.arange(1, 15)
    category_totals = category_totals.reindex(days_range, fill_value=0) # Set date range
    category_percentage = category_totals.div(category_totals.sum(axis=1), axis=0)

    # Plot settings
    plt.figure(figsize=(10, 6)) # Adjust the figsize as needed
    category_colors = sns.color_palette("hls", n_colors=len(category_list))
    category_percentage.plot(kind='area', stacked=True, color=category_colors)
    plt.title('Total Category Percentage per Day for All Users')
    plt.xlabel('Days')
    plt.ylabel('Percentage')

    # Set x-axis ticks and labels
    x_ticks = days_range
    x_labels = [f'Day {i}' for i in x_ticks]
    plt.xticks(x_ticks, x_labels, rotation=45)

    # Set x-axis range
    plt.xlim(days_range[0], days_range[-1])

    # Set legend
    plt.legend(title='Category')

    # Adjust layout
    plt.tight_layout()

    # Output path for the PNG file
    output_path = f'../../../data/img/soft_and_hard/total_duration/100%_stacked_area_chart/all/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the figure
    plt.savefig(output_path)
    plt.close()

    print(f'{output_path} output completed.')

# Load datasets
df_app = pd.read_csv('../../../data/csv/soft_and_hard/APP.csv', dtype={'user': str})
df_tv = pd.read_csv('../../../data/csv/soft_and_hard/TV.csv', dtype={'user': str})

# Plot and save total category percentage for each dataset
plot_total_category_percentage(df_app, 'app_100%_stacked_area_chart.png')
plot_total_category_percentage(df_tv, 'tv_100%_stacked_area_chart.png')
