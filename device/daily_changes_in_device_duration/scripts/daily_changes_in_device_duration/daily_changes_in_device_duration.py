import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_daily_viewing_time(df, file_name):
     # Calculate total daily viewing time
     daily_totals = df.groupby('days')['viewing_time'].sum()

     # Graph settings
     plt.figure(figsize=(10, 6))
     daily_totals.plot(kind='bar', color=sns.color_palette("hls", 1))

     plt.title('Device All Users Viewing Time per Day')
     plt.xlabel('Days')
     plt.ylabel('Total Viewing Time')

     # Set X-axis label
     plt.xticks(rotation=45)

     # Adjust layout
     plt.tight_layout()

     output_path = f'../../img/daily_changes_in_device_duration/all/{file_name}'
     os.makedirs(os.path.dirname(output_path), exist_ok=True)

     plt.savefig(output_path)
     plt.close()
     print(f'{output_path} output completed.')

df = pd.read_csv('../../data/csv/remove_outliers/device_add_days_viewing_time_del_outliers_iqr.csv', dtype={'user': str})

plot_daily_viewing_time(df, 'daily_viewing_time.png')
