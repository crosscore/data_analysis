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

# Function to plot total duration comparison for a single user
def plot_user_duration_comparison(df1, df2, user, ax, title_suffix):
    # Filter data for the given user
    df1_user = df1[df1['user'] == user]
    df2_user = df2[df2['user'] == user]

    # Calculate total duration for each source name in each user's dataset
    total_duration_df1_user = df1_user.groupby('source_name')['duration'].sum().reset_index()
    total_duration_df2_user = df2_user.groupby('source_name')['duration'].sum().reset_index()

    # Merge the two dataframes for comparison
    merged_df_user = pd.merge(total_duration_df1_user, total_duration_df2_user, on='source_name', 
                              suffixes=('_exp1', '_exp2'), how='outer').fillna(0)

    # Melting the dataframe for easier plotting
    melted_df_user = pd.melt(merged_df_user, id_vars='source_name', var_name='experiment', value_name='total_duration')

    # Plot for the user
    sns.barplot(x='source_name', y='total_duration', hue='experiment', data=melted_df_user, ax=ax)
    ax.set_title(f'User {user} {title_suffix}')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(labelrotation=90)

# Function to plot total duration comparison for the top 15 users
def plot_top_users_duration_comparison(df1, df2, title):
    # Get the top 15 users based on the number of records
    top_users = df['user'].value_counts().head(15).index.tolist()

    # Create a 3x5 grid of subplots
    fig, axs = plt.subplots(3, 5, figsize=(20, 12), constrained_layout=True)
    axs = axs.flatten()
    
    for i, user in enumerate(top_users):
        plot_user_duration_comparison(df1, df2, user, axs[i], title)

    # Adjust the layout
    plt.subplots_adjust(hspace=0.5, wspace=0.4)
    for ax in axs[len(top_users):]:
        ax.remove()  # Remove unused subplots

    # Save the figure
    file_name = 'top_users_duration_comparison.png'
    output_path = f'../../data/img/duration_comparison/top_users/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

    print(f'{output_path} output completed.')

# Load dataset
df = pd.read_csv('../../data/csv/concat_and_IQR/MBapp_TV_with_category.csv', dtype={'user': str})
df['date'] = df['date'].apply(unify_time_format)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

# Split the data into two dataframes based on the specified date range
start_date = '2022-10-22'
end_date = '2022-11-04'
df_exp1 = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
df_exp2 = df[(df['date'] < start_date) | (df['date'] > end_date)]

# Plot and save the comparison graph for the top 15 users
plot_top_users_duration_comparison(df_exp1, df_exp2, 'Total Duration Comparison Between Experiments')
