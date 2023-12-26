#add_duration.py
import pandas as pd
from datetime import datetime, timedelta

df = pd.read_csv('../../data/csv/add_duration/device_add_duration.csv', dtype={'user': str})
print(df)