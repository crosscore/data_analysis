import pandas as pd

df = pd.read_csv("../../csv/mobile/original/warehouse/TV_fix.csv", dtype={'user': str})

# Recalculate 'group' column
df['group'] = ((df['user'] != df['user'].shift()) |
                (df['program_name'] != df['program_name'].shift()) |
                (df['start_viewing_date'] != df['start_viewing_date'].shift()) |
                (df['genre_name'] != df['genre_name'].shift())).cumsum()
print(df)

# Calculate the total duration for each group
grouped = df.groupby('group').agg({
    'user': 'first',
    'start_viewing_date': 'first',
    'duration': 'sum',
    'program_name': 'first',
    'genre_name': 'first',
}).reset_index(drop=True)

print(grouped)
grouped.to_csv("../../csv/mobile/original/warehouse/TV_fix_duration.csv", index=False)