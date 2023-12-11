import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import glob
import os


file_names = glob.glob('./data/pod_data/latest/[0-9][0-9][0-9][0-9].csv')

for file_name in file_names:
    user_id = os.path.basename(file_name).split('.')[0]
    data = pd.read_csv(file_name, parse_dates=['eliminate_date'])

    check_data = data[data['action'] == 'check'].copy()
    check_data['hour'] = check_data['eliminate_date'].dt.hour

    check_counts = check_data.groupby(['hour', 'device_id']).size().reset_index(name='check_count')

    all_hours = pd.DataFrame({'hour': list(range(24))})
    all_device_ids = pd.DataFrame({'device_id': [0, 1, 2, 3]})
    complete_index = all_hours.merge(all_device_ids, how='cross')

    check_counts = check_counts.merge(complete_index, on=['hour', 'device_id'], how='right').fillna(0)

    def map_device_id(device_id):
        mapping = {
            0: 'Washroom',
            1: 'Kitchen',
            2: 'Living room',
            3: 'Work place'
        }
        return mapping.get(device_id, f'Unknown ID: {device_id}')

    check_counts['Location'] = check_counts['device_id'].apply(map_device_id)
    print(check_counts)

    sns.set(style="darkgrid")

    g = sns.catplot(
        data=check_counts, x='hour', y='check_count', hue='Location',
        kind='bar', height=7, aspect=2, palette="muted"
    )

    g.ax.set_ylim(0, 60)
    
    g._legend.set_bbox_to_anchor((1, 0.5))

    plt.get_current_fig_manager().set_window_title(f'Aggregated results for user {user_id}')  # Set window title
    g.set_axis_labels('24 hour format', f'Total number of checks for user {user_id}')
    g.ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))  # Format x-axis labels as integers
    g.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

    plt.savefig(f'Img_Check_User_{user_id}.png')
    plt.close()
