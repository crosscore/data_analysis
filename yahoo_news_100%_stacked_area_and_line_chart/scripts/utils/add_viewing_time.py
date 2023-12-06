#add_viewing_time.py
import pandas as pd

df = pd.read_csv('../../data/csv/device_with_category.csv', dtype={'user': str})
print(df)