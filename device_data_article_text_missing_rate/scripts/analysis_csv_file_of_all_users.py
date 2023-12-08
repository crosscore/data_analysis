import pandas as pd

df = pd.read_csv("../data/csv/csv_and_json/all_user_plus_json.csv", dtype={'user': str})
print(df)
#dfの'user'列の値毎に'action'の値が'view'である行の合計値を出力
sum = 0
for user in df['user'].unique():
    print(user, df[df['user'] == user]['action'].value_counts()['view'])
    sum += df[df['user'] == user]['action'].value_counts()['view']

print(sum)

# view_df = df[df['action'] == 'view']
# view_counts = view_df.groupby('user').size()
# print(view_counts)