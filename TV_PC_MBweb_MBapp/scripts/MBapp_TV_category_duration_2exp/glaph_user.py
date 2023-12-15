import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
df = pd.read_csv('../../data/csv/concat_and_IQR/MBapp_TV_with_category.csv', dtype={'user': str})

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d %H:%M:%S', errors='coerce')

# Split the data into two dataframes based on the specified date range
start_date = '2022-10-22'
end_date = '2022-11-04'
df_exp1 = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
df_exp2 = df[(df['date'] < start_date) | (df['date'] > end_date)]

# Get all unique users and source names
users = df['user'].unique()
source_names = df['source_name'].unique()

# Displays the total value of duration for both experimental periods for each source_name
for source_name in source_names:
    total_duration_exp1 = df_exp1[df_exp1['source_name'] == source_name]['duration'].sum()
    total_duration_exp2 = df_exp2[df_exp2['source_name'] == source_name]['duration'].sum()
    print(f"Source Name: {source_name}")
    print(f"  Experiment 1 Total Duration: {total_duration_exp1}")
    print(f"  Experiment 2 Total Duration: {total_duration_exp2}\n")


# Create a figure to contain the subplots
fig, axes = plt.subplots(15, 4, figsize=(20, 30))  # 15 users, 4 source_names

for i, user in enumerate(users):
    for j, source_name in enumerate(source_names):
        # Position for each subplot
        ax = axes[i, j % 4]

        # Filter data for the specific user and source name
        df1_user_source = df_exp1[(df_exp1['user'] == user) & (df_exp1['source_name'] == source_name)]
        df2_user_source = df_exp2[(df_exp2['user'] == user) & (df_exp2['source_name'] == source_name)]

        # Calculate total duration for each experiment
        total_duration_exp1 = df1_user_source['duration'].sum()
        total_duration_exp2 = df2_user_source['duration'].sum()

        # Prepare data for plotting
        data = {
            'Experiment': ['exp1', 'exp2'],
            'Total Duration': [total_duration_exp1, total_duration_exp2]
        }
        df_plot = pd.DataFrame(data)

        # Plot
        sns.barplot(x='Experiment', y='Total Duration', data=df_plot, ax=ax)
        ax.set_title(f'User {user} - {source_name}')
        ax.set_xlabel('')
        ax.set_ylabel('')

        # Hide x-axis labels to prevent overlap
        if i < 14:  # Only hide for rows except for the last one
            ax.set_xticklabels([])
        else:
            ax.set_xticklabels(['exp1', 'exp2'], rotation=45)

        # Hide y-axis labels to prevent overlap
        if j > 0:
            ax.set_yticklabels([])

# Adjust layout
plt.tight_layout()

# Save the figure
output_path = '../../data/img/duration_comparison/user/total_duration_comparison_user.png'
plt.savefig(output_path)
plt.close()

print(f'Graph saved at {output_path}')
