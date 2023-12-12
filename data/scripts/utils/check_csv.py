import pandas as pd

df = pd.read_csv("../../csv/device/all/all_device.csv", dtype={'user': str})
print(df)