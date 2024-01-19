import pandas as pd

df = pd.read_csv("../../data/csv/add_days/device.csv", dtype={'user': str})
print(df)

df.loc[df['days'] <= 7, 'period'] = 'EP1'
df = df.sort_values(['period', 'user', 'date'])

print(df)
df.to_csv("../../data/csv/add_days/device_EP.csv", index=False)