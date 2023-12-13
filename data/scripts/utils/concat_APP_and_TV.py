#concat_APP_and_TV.py
import pandas as pd
from datetime import datetime

df_tv = pd.read_csv("../../csv/mobile/original/TV_APP/original/TV_fix_duration.csv", dtype={'user': str})
df_app = pd.read_csv("../../csv/mobile/original/TV_APP/original/APP_fix.csv", dtype={'user': str})

df_tv = df_tv[['user', 'date', 'duration', 'tv_category']]
df_app = df_app[['user', 'date', 'duration', 'app_category']]

# Function to convert a date column to a datetime object and reformat it in a uniform format
def unify_date_format(df, date_column):
     df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
     df[date_column] = df[date_column].dt.strftime('%Y/%m/%d %H:%M')
     return df

# Apply function to TV and APP data frame
df_tv = unify_date_format(df_tv, 'date')
df_app = unify_date_format(df_app, 'date')
df_tv = df_tv.dropna(subset=['tv_category'])
df_app = df_app.dropna(subset=['app_category'])

print(df_tv['tv_category'].value_counts(dropna=False))
print('--------------')
print(df_app['app_category'].value_counts(dropna=False))

df = pd.concat([df_tv, df_app])
df = df.sort_values(by=['user', 'date'])
print(df)
df.to_csv("../../csv/mobile/original/TV_APP/TV_APP.csv", index=False)