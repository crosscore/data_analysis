import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_and_save_total_duration(df, file_name):
    # Calculate total duration for each day
    total_duration_by_day = df.groupby('days')['duration'].sum()

    # Ensure all days from 1 to 14 are present
    days_range = pd.Series(range(1, 15), name='days')
    total_duration_by_day = total_duration_by_day.reindex(days_range, fill_value=0)

    # Plot
    plt.figure(figsize=(10, 6)) # Adjust the figsize as needed
    total_duration_by_day.plot(kind='bar', color='skyblue')
    plt.title('Total Duration per Day for All Users')
    plt.xlabel('Days')
    plt.ylabel('Total Duration')

    plt.tight_layout()

    output_path = f'../../../data/img/soft_and_hard/average_daily_duration/all/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.savefig(output_path)
    plt.close()

    print(f'{output_path} output completed.')

# Load datasets
df_app = pd.read_csv('../../../data/csv/soft_and_hard/APP.csv', dtype={'user': str})
df_tv = pd.read_csv('../../../data/csv/soft_and_hard/TV.csv', dtype={'user': str})

# Plot and save total duration for each dataset
plot_and_save_total_duration(df_app, 'app_all_bar_chart.png')
plot_and_save_total_duration(df_tv, 'tv_all_bar_chart.png')

