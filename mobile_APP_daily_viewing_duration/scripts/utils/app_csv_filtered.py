# APP.csvのヘッダーをheadrs_to_extractに限定

import csv

input_file = './original/fix/APP.csv'
output_file = './filtered/APP_filtered.csv'

headers_to_extract = [
    'user', 'date', 'duration', 'os', 'package_id',
    'app_category', 'app_provider_name', 'app_name'
]

with open(input_file, newline='', encoding='utf-8-sig') as infile, \
        open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=headers_to_extract)
    print(f'Input file headers: {reader.fieldnames}\n')
    
    writer.writeheader()
    print(f'Output file headers: {writer.fieldnames}')
    for row in reader:
        # 'user' フィールドの値を明示的に文字列に変換
        row['user'] = str(row.get('user', '')).zfill(4)
        writer.writerow({field: row.get(field, '') for field in headers_to_extract})
