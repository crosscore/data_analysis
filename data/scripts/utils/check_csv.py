import pandas as pd

df = pd.read_csv("../../json/json_data_no_body.csv", dtype={'user': str})
print(df['title'].str.len().max())
print('------')
print(df['title'].str.len().min())
print('------')
print(df[df['title'].str.len() == 4]['title'])