# add_duration.py
import pandas as pd
from datetime import datetime, timedelta

category_dict = {'国内': 'domestic', 
                 '国際': 'world', 
                 '経済': 'business',
                 'エンタメ': 'entertainment',
                 'スポーツ': 'sports',
                 '地域': 'local',
                 'ライフ': 'life',
                 'IT': 'it', 
                 '科学': 'science'}

def process_row(row):
    # Duration calculation
    start = datetime.fromisoformat(row['start_viewing_date'])
    stop = datetime.fromisoformat(row['stop_viewing_date'])
    duration = int((stop - start).total_seconds())

    # Category translation
    translated_category = category_dict.get(row['category'], row['category'])

    return pd.Series([duration, translated_category], index=['duration', 'translated_category'])

df = pd.read_csv('../../data/csv/1st_half_and_2nd_half/device_original_1st_half_and_2nd_half.csv', dtype={'user': str})
print(df)

# Apply process_row function to each row and create new columns
df[['duration', 'translated_category']] = df.apply(process_row, axis=1)

# Update category with translated values
df['category'] = df['translated_category']
df.drop(columns=['translated_category'], inplace=True)

# Keep only the required columns and filter out negative durations
df = df[['user', 'category', 'duration', 'days']]
df = df[df['duration'] >= 0]

# Save to new CSV
df.to_csv('../../data/csv/add_duration/device_all_category_add_duration.csv', index=False)

# Print modified dataframe and category counts
print(df)
print(df['category'].value_counts(dropna=False))
