import pandas as pd
import glob

filename = glob.glob('./??.csv')

all_data = pd.DataFrame()
for file in filename:
    data = pd.read_csv(file, dtype={'User': str})
    data['media'] = file.split('\\')[1].split('.')[0]
    all_data = pd.concat([all_data, data])

all_data.to_csv('media.csv', index=False)
