import pandas as pd

df = pd.read_csv("../../csv/mobile/original/warehouse/TV_fix.csv", dtype={'user': str})
print(df)

df = df[['user', 'date', 'duration', 'program_name', 'start_viewing_date', 'stop_viewing_date', 'genre_name']]
print(df)

df.to_csv("../../csv/mobile/original/warehouse/TV_fix_new.csv", index=False)