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

# Calculate the total duration decrease for each app_category in each period
def calculate_duration_decrease(df1, df2, category_col):
    total_duration_exp1 = df1.groupby(category_col)['duration'].sum()
    total_duration_exp2 = df2.groupby(category_col)['duration'].sum()
    duration_difference = total_duration_exp1 - total_duration_exp2
    decreased_categories = duration_difference[duration_difference > 0]
    return decreased_categories

decreased_mb_categories = calculate_duration_decrease(df_mb[df_mb['date'].isin(df_exp1['date'])],
                                                      df_mb[df_mb['date'].isin(df_exp2['date'])],
                                                      'app_category')

decreased_tv_categories = calculate_duration_decrease(df_tv[df_tv['date'].isin(df_exp1['date'])],
                                                      df_tv[df_tv['date'].isin(df_exp2['date'])],
                                                      'tv_category')

def plot_decreased_categories(decreased_categories, title, output_path):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=decreased_categories.index, y=decreased_categories.values, palette='hls')
    plt.title(title)
    plt.ylabel('Duration Decrease')
    plt.xticks(rotation=270)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

output_path_mb = '../../data/img/categories_with_decreased_viewing_time/all/decrease_duration_per_app_category.png'
output_path_tv = '../../data/img/categories_with_decreased_viewing_time/all/decrease_duration_per_tv_category.png'
os.makedirs(os.path.dirname(output_path_mb), exist_ok=True)
os.makedirs(os.path.dirname(output_path_tv), exist_ok=True)

plot_decreased_categories(decreased_mb_categories, 'Decrease in Duration per App Category', output_path_mb)
plot_decreased_categories(decreased_tv_categories, 'Decrease in Duration per TV Category', output_path_tv)
