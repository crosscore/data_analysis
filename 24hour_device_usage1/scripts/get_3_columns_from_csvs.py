import csv

csv_list = ['APP', 'MBWEB', 'PCWEB']

def process_csv(input_filename, output_filename):
    with open(f'{input_filename}.csv', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        with open(f'Formatted_csv/{output_filename}.csv', 'w', newline='', encoding='utf-8') as outfile:
            csvwriter = csv.writer(outfile)
            header = next(csvreader)

            # 必要な列のインデックスを取得
            device_no_index = header.index('\ufeff機器番号') #0
            date_time_index = header.index('日時(yyyy-mm-dd hh:mm:ss)') #6
            duration_index = header.index('接触時間（duration)') #10

            csvwriter.writerow(['ID', 'Viewing_Start_Time', 'Viewing_Duration'])
            for row in csvreader:
                csvwriter.writerow([row[device_no_index], row[date_time_index], row[duration_index]])

for csv_name in csv_list:
    process_csv(csv_name, f'{csv_name}_formatted.csv')
