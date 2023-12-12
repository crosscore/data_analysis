import pandas as pd

device_df = pd.read_csv('../../csv/device/all/all_device.csv', dtype={'user': str})
json_df = pd.read_csv('../../json/json_data_no_body.csv')

# Identify duplicate rows in 'url' column
duplicated_urls = json_df[json_df.duplicated('url', keep=False)]

# json_dfを'url'でソート
json_df = json_df.sort_values(by='url')
json_df.to_csv('../../json/json_data_no_body_sort_urls.csv', index=False)

# Output the number of duplicate URLs
print(f"Number of duplicated URLs: {duplicated_urls['url'].nunique()}")

# Option: Export duplicate URL data to CSV
#duplicated_urls.to_csv('../../json/json_data_duplicated_urls.csv', index=False)

#Inner join a and b based on the value of the 'url' column
merged_df = pd.merge(device_df, json_df, on='url', how='inner')
print(merged_df)
merged_df.to_csv('../../csv+json/all_device_json.csv', index=False)

# Create a list of URLs used for merge
merged_urls = merged_df['url'].unique()
#merged_urls = list(merged_urls)
print(f'{len(merged_urls)}')

# Exclude rows with URLs used for join from json_df
unmatched_json_df = json_df[~json_df['url'].isin(merged_urls)]
unmatched_json_df = unmatched_json_df[['url', 'title']]
unmatched_json_df.to_csv('../../csv+json/unmatched_json_data.csv', index=False)
print(unmatched_json_df)