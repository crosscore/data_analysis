import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_and_save(df, file_name):
    fig, axes = plt.subplots(5, 3, figsize=(15, 25)) # Adjust the figsize as needed
    axes = axes.flatten() # Flatten the axes array for easy indexing

    for i, user in enumerate(df['user'].unique()[:15]): # Limit to first 15 users
        user_df = df[df['user'] == user]

        # Ensure all days from 1 to 14 are present
        days_range = pd.Series(range(1, 15), name='days')
        user_df = user_df.groupby('days')['duration'].mean().reindex(days_range, fill_value=0)

        user_df.plot(kind='bar', color='skyblue', ax=axes[i])
        axes[i].set_title(f'User {user}')
        axes[i].set_xlabel('Days')
        axes[i].set_ylabel('Average Duration')

    plt.tight_layout()

    output_path = f'../../../data/img/soft_and_hard/average_daily_duration/user/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.savefig(output_path)
    plt.close()

    print(f'{output_path} output completed.')

# Load datasets
df_app = pd.read_csv('../../../data/csv/soft_and_hard/APP.csv', dtype={'user': str})
df_tv = pd.read_csv('../../../data/csv/soft_and_hard/TV.csv', dtype={'user': str})

# Plot and save for each dataset
plot_and_save(df_app, 'app_users_bar_chart.png')
plot_and_save(df_tv, 'tv_users_bar_chart.png')
