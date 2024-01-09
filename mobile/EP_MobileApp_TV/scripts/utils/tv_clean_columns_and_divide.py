import pandas as pd

df = pd.read_csv("../../data/csv/original/TV_before_add_duration_fix_user.csv", dtype={'user': str})

#user,TVエリア,性年代,メディアターゲット区分,仕事環境,最終学歴,date,duration,視聴フラグ(RT/TS),channel,program_name,番組放映開始日時,番組放映終了日時,genre_name

# clean columns
df = df[['user', 'date', 'duration', 'genre_name']]

# sort df by 'user' and 'date'
df.sort_values(by=['user', 'date'], ascending=[True, True], inplace=True)
print(df)

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'])

# Define the date range
start_date = '2022-10-22'
end_date = '2022-11-04'

# Filter data based on the date range
df_exp1 = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
df_exp2 = df[(df['date'] < start_date) | (df['date'] > end_date)]

# Output to CSV files
df_exp1.to_csv('../../data/csv/original/divide_by_exp/TV_exp1.csv', index=False)
df_exp2.to_csv('../../data/csv/original/divide_by_exp/TV_exp2.csv', index=False)

print(df_exp1['genre_name'].unique())