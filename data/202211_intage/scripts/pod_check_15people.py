import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import glob

file_names = glob.glob('./data/pod_data/latest/[0-9][0-9][0-9][0-9].csv')

all_data = pd.DataFrame()
for file_name in file_names:
    data = pd.read_csv(file_name, parse_dates=['eliminate_date'])
    all_data = pd.concat([all_data, data])

check_data = all_data[all_data['action'] == 'check'].copy()
check_data['hour'] = check_data['eliminate_date'].dt.hour

check_counts = check_data.groupby(['hour', 'device_id']).size().reset_index(name='view_count')

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

# Create the bar plot
g = sns.catplot(
    data=check_counts, x='hour', y='view_count', hue='Location',
    kind='bar', height=7, aspect=2, palette="muted"
)

g._legend.set_bbox_to_anchor((1, 0.5))

plt.get_current_fig_manager().set_window_title('Analysis results of checks for 15 people')  # Set window title
g.set_axis_labels('24 hour format', 'Total number of checks for all 15 people')
g.ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))  # Format x-axis labels as integers
g.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

#plt.show()
plt.savefig('Img_Check_15people.png')
plt.close()