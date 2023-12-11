import pandas as pd

df = pd.read_json('../json/all_user.json')

df_extracted = df['Item'].apply(pd.Series)[['url', 'title']].applymap(lambda x: x['S'])

df_extracted.to_csv('../json/json_data_no_body.csv', index=False)
print(df_extracted)
