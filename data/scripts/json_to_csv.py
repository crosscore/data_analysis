import pandas as pd

df = pd.read_json('../json/all_user.json')

df_extracted = df['Item'].apply(pd.Series)[['url', 'published_date', 'title', 'body']].applymap(lambda x: x['S'])

df_extracted.to_csv('../json/json_original.csv', index=False)
print(df_extracted)

# df_extracted's unique 'url' rows count
print(df_extracted['url'].nunique())

#Output only rows where the value of the 'body' column of df_extracted is ''
df_body_empty = df_extracted[df_extracted['body'] == '']
df_body_empty.to_csv('../json/json_body_empty.csv', index=False)

#Output only rows where the value of the 'title' column of df_extracted is ''
df_title_empty = df_extracted[df_extracted['title'] == '']
df_title_empty.to_csv('../json/json_title_empty.csv', index=False)

#Output only rows where the value of the 'url' column of df_extracted is ''
df_url_empty = df_extracted[df_extracted['url'] == '']
df_url_empty.to_csv('../json/json_url_empty.csv', index=False)
