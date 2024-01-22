import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def unify_time_format(time_str):
    parts = time_str.split(':')
    if len(parts) == 2:
        return time_str + ":00"
    return time_str

def plot_userwise_duration_comparison(df, start_date, end_date, title):
    # Divide each user's data frame by experiment period
    df_exp1 = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    df_exp2 = df[(df['date'] < start_date) | (df['date'] > end_date)]

    # Calculate the total source name duration for each user
    user_duration_exp1 = df_exp1.groupby(['user', 'source_name'])['duration'].sum().reset_index()
    user_duration_exp2 = df_exp2.groupby(['user', 'source_name'])['duration'].sum().reset_index()

    # Get the total number of users and select the top 15 users
    top_users = df['user'].value_counts().index[:15]

    # Generate subplots with 3x5 grid
    fig, axes = plt.subplots(3, 5, figsize=(20, 12), sharex=True, sharey=True)
    axes = axes.flatten()
    
    for i, user in enumerate(top_users):
        ax = axes[i]
        
        # Get data for each user
        user_exp1 = user_duration_exp1[user_duration_exp1['user'] == user]
        user_exp2 = user_duration_exp2[user_duration_exp2['user'] == user]
    
        # Merge data and compare experimental periods 1 and 2
        user_merged = pd.merge(user_exp1, user_exp2, on='source_name', suffixes=('_exp1', '_exp2'), how='outer').fillna(0)
        user_melted = pd.melt(user_merged, id_vars='source_name', var_name='experiment', value_name='total_duration')

        # draw bar graph
        sns.barplot(x='source_name', y='total_duration', hue='experiment', data=user_melted, ax=ax)
        ax.set_title(f'User: {user}')
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.tick_params(labelrotation=90)

    # Set the overall title and label
    fig.suptitle(title, fontsize=16)
    fig.text(0.5, 0.04, 'Source Name', ha='center', va='center')
    fig.text(0.06, 0.5, 'Total Duration', ha='center', va='center', rotation='vertical')

     # save plot
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    file_name = 'userwise_duration_comparison.png'
    output_path = f'../../data/img/duration_comparison/userwise/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} output completed.')

df = pd.read_csv('../../data/csv/concat_and_IQR/MBapp_TV_with_category.csv', dtype={'user': str})
df['date'] = df['date'].apply(unify_time_format)
df['date'] = pd.to_datetime(df['date'], dayfirst=True)

plot_userwise_duration_comparison(df, '2022-10-22', '2022-11-04', 'User-wise Total Duration Comparison Between Experiments')
