import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import japanize_matplotlib

df = pd.read_csv('../../data/csv/concat_and_IQR/MBapp_TV_with_category.csv', dtype={'user': str})

df['date'] = pd.to_datetime(df['date'])

# Split data based on experiment period
start_date_exp1 = '2022-10-22'
end_date_exp1 = '2022-11-04'
df_exp1 = df[(df['date'] >= start_date_exp1) & (df['date'] <= end_date_exp1)]
df_exp2 = df[(df['date'] < start_date_exp1) | (df['date'] > end_date_exp1)]

# Split data based on source_name
df_mb = df[df['source_name'] == 'MobileApp']
df_tv = df[df['source_name'] == 'TV']

# Calculate the duration difference for each category in each period
def calculate_duration_difference(df1, df2, category_col):
    total_duration_exp1 = df1.groupby(category_col)['duration'].sum()
    total_duration_exp2 = df2.groupby(category_col)['duration'].sum()
    duration_difference = total_duration_exp2 - total_duration_exp1
    return duration_difference

duration_difference_mb = calculate_duration_difference(df_mb[df_mb['date'].isin(df_exp1['date'])],
                                                       df_mb[df_mb['date'].isin(df_exp2['date'])],
                                                       'app_category')

duration_difference_tv = calculate_duration_difference(df_tv[df_tv['date'].isin(df_exp1['date'])],
                                                       df_tv[df_tv['date'].isin(df_exp2['date'])],
                                                       'tv_category')

def plot_duration_difference(difference, title, output_path):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=difference.index, y=difference.values, palette='hls')
    plt.title(title)
    plt.ylabel('Duration Difference')
    plt.xticks(rotation=270)
    plt.axhline(0, color='gray', linestyle='--')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

output_path_mb = '../../data/img/categories_duration_difference/app_category.png'
output_path_tv = '../../data/img/categories_duration_difference/tv_category.png'
os.makedirs(os.path.dirname(output_path_mb), exist_ok=True)
os.makedirs(os.path.dirname(output_path_tv), exist_ok=True)

plot_duration_difference(duration_difference_mb, 'Duration Difference per App Category', output_path_mb)
plot_duration_difference(duration_difference_tv, 'Duration Difference per TV Category', output_path_tv)
