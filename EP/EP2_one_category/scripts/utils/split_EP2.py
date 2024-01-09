import pandas as pd

df = pd.read_csv("../../data/csv/outlier_removed/MobileApp_EP_outlier_removed.csv", dtype={'user': str})
print(df)

# dfの'period'列の値が'EP2'の行のみを抽出
df = df[df['period'] == 'EP2']

df.loc[df['days'] <= 7, 'period'] = 'EP1'
df = df.sort_values(['period', 'user', 'date'])

print(df)
df.to_csv("../../data/csv/complete/MobileApp.csv", index=False)