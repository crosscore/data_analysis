import pandas as pd

df_app = pd.read_csv('../../data/csv/add_days/APP_add_days.csv', dtype={'user': str})
print(df_app['app_category'].unique())