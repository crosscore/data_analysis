import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np
import japanize_matplotlib

df = pd.read_csv('../../../../data/csv/soft_and_hard/z-score/device_add_days_viewing_time_del_outliers_soft_hard.csv', dtype={'user': str})

for user in df['user'].unique():
    user_df = df[df['user'] == user]

    # Calculate the average value of 'viewing_time' for each 'days' column
    average_viewing_time = user_df.groupby('days')['viewing_time'].mean()

    # Graph settings
    plt.figure(figsize=(10, 6))
    average_viewing_time.plot(kind='bar', color='skyblue')

    # Set graph title and axis labels
    plt.title(f'User {user} Average daily viewing time')
    plt.xlabel('Days')
    plt.ylabel('Average viewing time')

    output_path = f'../../../../data/img/soft_and_hard/z-score/average_viewing_time_by_day/user/{user}_bar_chart.png'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} output completed.')
