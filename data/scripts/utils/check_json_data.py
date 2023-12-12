import pandas as pd

json_file = pd.read_csv('../../json/json_data_no_body.csv', dtype={'user': str})
print(json_file)