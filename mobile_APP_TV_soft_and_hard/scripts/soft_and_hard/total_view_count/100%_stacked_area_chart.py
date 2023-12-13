#yahoo_news_100%_stacked_area_chart.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

df = pd.read_csv('../../../../data/csv/soft_and_hard/iqr/device_add_days_viewing_time_del_outliers_soft_hard.csv', dtype={'user': str})
#category_list = ['国内', '国際', '経済', 'エンタメ', 'スポーツ', 'IT', '科学', 'ライフ', '地域']
category_list = ['soft_news', 'hard_news']

# Process data
category_totals = df.groupby(['days', 'category']).size().unstack(fill_value=0).reindex(columns=category_list, fill_value=0)

# ensure date range
days_range = np.arange(1, 15)
category_totals = category_totals.reindex(days_range, fill_value=0) # Set date range

# Calculate the percentage of each category (for 100% stacked area chart)
category_percentage = category_totals.div(category_totals.sum(axis=1), axis=0)

# Settings common to all graphs
fig, ax = plt.subplots(1, 1, figsize=(10, 6))
x_ticks = days_range
x_labels = [f'Day {i}' for i in x_ticks]

# Create a 100% stacked area chart
category_colors = sns.color_palette("hls", n_colors=len(category_list))
category_percentage.plot(kind='area', stacked=True, color=category_colors, ax=ax)

ax.set_title('Percentage of views by category for all users')
ax.set_ylabel('percentage')
ax.set_xlabel('Days')

# set x-axis ticks and labels
ax.set_xticks(x_ticks)
ax.set_xticklabels(x_labels, rotation=45)

# set x-axis range
ax.set_xlim(days_range[0], days_range[-1])

# set legend
handles, labels = ax.get_legend_handles_labels()
handles = [handles[labels.index(cat)] for cat in category_list if cat in labels]
labels = [label for label in category_list if label in labels]
ax.legend(handles, labels, title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')

output_path = '../../../../data/img/soft_and_hard/iqr/analysis_by_total_view_count/100%_stacked_area_chart/all/stacked_area_chart.png'
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.tight_layout()
plt.savefig(output_path)
plt.close()
print(f'{output_path} was output.')
