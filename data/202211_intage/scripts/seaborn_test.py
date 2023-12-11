import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob

file_names = glob.glob('./data/pod_data/latest/[0-9][0-9][0-9][0-9].csv')
all_data = pd.DataFrame()
for file_name in file_names:
    data = pd.read_csv(file_name, parse_dates=['start_viewing_date'])
    all_data = pd.concat([all_data, data])

view_data = all_data[all_data['action'] == 'view'].copy()
view_data['hour'] = view_data['start_viewing_date'].dt.hour

view_counts = view_data.groupby(['hour', 'device_id']).size().reset_index(name='view_count')

sns.set(style="darkgrid")

g = sns.catplot(
    data=view_counts, x='hour', y='view_count', hue='device_id',
    kind='bar', height=6, aspect=2, palette="muted"
)

plt.get_current_fig_manager().set_window_title('集計結果')
g.set_axis_labels('24 hour format', 'Total number of views')
g.set_xticklabels([int(tick) for tick in g.ax.get_xticks()])

plt.show()
#plt.savefig('output.png')