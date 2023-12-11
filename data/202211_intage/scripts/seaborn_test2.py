import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob

user_ids = ['0765', '0816', '1143', '2387', '2457', '3613', '3828', '4545', '4703', '5711', '5833', '6420', '7471', '8058', '9556']

all_data = pd.DataFrame()

# Read each user's data and combine into all_data
for user_id in user_ids:
     file_name = f'./data/pod_data/latest/{user_id}.csv'
     data = pd.read_csv(file_name, parse_dates=['start_viewing_date'])
     data['user_id'] = user_id # add user_id column
     all_data = pd.concat([all_data, data])
print(all_data)

# Filter only rows where 'action' column is 'view'
view_data = all_data[all_data['action'] == 'view'].copy()
view_data['hour'] = view_data['start_viewing_date'].dt.hour
print(view_data)

# Aggregate the number of views by 'hour' and 'user_id'
view_counts = view_data.groupby(['hour', 'user_id']).size().reset_index(name='view_count')

# Create a function to map the value of device_id
def map_device_id(device_id):
     mapping = {
         0: 'Washroom',
         1: 'Kitchen',
         2: 'Living room',
         3: 'Work place'
     }
     return mapping.get(device_id, f'Unknown ID: {device_id}')

# update the value of device_id column
#view_counts['Location'] = view_counts['device_id'].apply(map_device_id)

sns.set(style="darkgrid")

# Create a graph for each user
for user_id in user_ids:
     filtered_data = view_counts[view_counts['user_id'] == user_id]
     g = sns.catplot(data=filtered_data, x='hour', y='view_count', kind='bar', height=8, aspect=2, palette="muted")
     plt.title(f'User ID: {user_id}')
     g.set_axis_labels('24 hour format', 'View Count')
     g.set_xticklabels([int(tick) for tick in g.ax.get_xticks()])
     g.ax.set_ylim(0, 250)
     plt.get_current_fig_manager().set_window_title(f'User ID: {user_id}')
     plt.subplots_adjust(top=0.9)
     plt.show()

# Create a graph of the overall results
aggregated_view_counts = view_counts.groupby('hour')['view_count'].sum().reset_index()
g_agg = sns.catplot(data=aggregated_view_counts, x='hour', y='view_count', kind='bar', height=8, aspect=2, palette="muted")
plt.title('Aggregated results for 15 people')
g_agg.set_axis_labels('24 hour format', 'Total number of views for all 15 people')
g_agg.set_xticklabels([int(tick) for tick in g_agg.ax.get_xticks()])
plt.get_current_fig_manager().set_window_title('Aggregated results for 15 people')
plt.subplots_adjust(top=0.9)

plt.show()
