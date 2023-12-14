import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_histogram(df, file_name, title):
    # Histogram settings
    plt.figure(figsize=(10, 6))
    plt.hist(df['duration'], bins=50, color='skyblue', edgecolor='black')

    # Set graph title and axis labels
    plt.title(title)
    plt.xlabel('Duration')
    plt.ylabel('Frequency')

    # Output path for the PNG file
    output_path = f'../../../data/img/soft_and_hard/histogram/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} has been printed.')

# Load datasets
df_app = pd.read_csv('../../../data/csv/soft_and_hard/APP.csv', dtype={'user': str})
df_tv = pd.read_csv('../../../data/csv/soft_and_hard/TV.csv', dtype={'user': str})

# Plot and save histogram for each dataset
plot_histogram(df_app, 'app/app_histogram.png', 'Distribution of Duration for APP')
plot_histogram(df_tv, 'tv/tv_histogram.png', 'Distribution of Duration for TV')
