import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

def plot_total_category_duration(df, file_name):
    # Calculate total duration for each category per day
    category_totals = df.groupby(['days', 'category'])['duration'].sum().unstack(fill_value=0)
    days_range = np.arange(1, 15)
    category_totals = category_totals.reindex(days_range, fill_value=0) # Ensure all days are included

    # Plot settings
    plt.figure(figsize=(10, 6)) # Adjust the figsize as needed
    category_totals.plot(kind='bar', stacked=True, color=sns.color_palette("hls", n_colors=len(category_totals.columns)))
    plt.title('Total Duration for All Users')
    plt.xlabel('Days')
    plt.ylabel('Total Duration')

    # Set x-axis ticks and labels
    x_labels = [f'Day {i}' for i in days_range]
    plt.xticks(np.arange(len(x_labels)), x_labels, rotation=45)

    # Set legend
    plt.legend(title='Category')

    # Adjust layout
    plt.tight_layout()

    # Output path for the PNG file
    output_path = f'../../../data/img/soft_and_hard/total_duration/bar_chart/all/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save the figure
    plt.savefig(output_path)
    plt.close()

    print(f'{output_path} output completed.')

# Load datasets
df_app = pd.read_csv('../../../data/csv/soft_and_hard/APP.csv', dtype={'user': str})
df_tv = pd.read_csv('../../../data/csv/soft_and_hard/TV.csv', dtype={'user': str})

# Plot and save total duration for each dataset
plot_total_category_duration(df_app, 'app_total_duration.png')
plot_total_category_duration(df_tv, 'tv_total_duration.png')
