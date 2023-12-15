import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

# Function to unify time format
def unify_time_format(time_str):
    # Split the time string by colon
    parts = time_str.split(':')

    # If there are only two parts (hours and minutes), add ":00" for seconds
    if len(parts) == 2:
        return time_str + ":00"
    return time_str

def plot_total_duration_comparison(df1, df2, title):
    # Calculate total duration for each source name in each dataset
    total_duration_df1 = df1.groupby('source_name')['duration'].sum().reset_index()
    total_duration_df2 = df2.groupby('source_name')['duration'].sum().reset_index()

    # Merge the two dataframes for comparison
    merged_df = pd.merge(total_duration_df1, total_duration_df2, on='source_name', suffixes=('_exp1', '_exp2'))
    print(merged_df)

    # Melting the dataframe for easier plotting
    melted_df = pd.melt(merged_df, id_vars='source_name', var_name='experiment', value_name='total_duration')

    # Plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='source_name', y='total_duration', hue='experiment', data=melted_df)
    plt.title(title)
    plt.xlabel('Source Name')
    plt.ylabel('Total Duration')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save plot
    file_name = 'total_duration_comparison.png'
    output_path = f'../../data/img/duration_comparison/all/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    print(f'{output_path} output completed.')

# Load dataset
df = pd.read_csv('../../data/csv/concat_and_IQR/MBapp_MBweb_PC_TV.csv', dtype={'user': str})
print(df)

# Apply the function to the 'time' column (replace 'time' with the actual name of your time column)
df['date'] = df['date'].apply(unify_time_format)

# Convert the 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# Split the data into two dataframes based on the specified date range
start_date = '2022-10-22'
end_date = '2022-11-04'
df_exp1 = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
df_exp2 = df[(df['date'] < start_date) | (df['date'] > end_date)]

# Plot and save the comparison graph
plot_total_duration_comparison(df_exp1, df_exp2, 'Total Duration Comparison Between Experiments')
