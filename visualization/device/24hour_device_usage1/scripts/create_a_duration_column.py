import csv

def process_tv_csv(input_filename, output_filename):
    with open(input_filename, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        header = next(csvreader) #1行目のラベルをスキップ
        
        id_index = header.index('\ufeff機器番号') #0
        datetime_index = header.index('日時(yyyy-mm-dd hh:mm:ss)') #6
        program_name_index = header.index('番組名') #10

        with open(f'{output_filename}.csv', 'w', newline='', encoding='utf-8') as outfile:
            csvwriter = csv.writer(outfile)
            csvwriter.writerow(['ID', 'Viewing_Start_Time', 'Viewing_Duration'])
            prev_program_name = None
            prev_datetime = None
            prev_id = None
            duration = 0
            for row in csvreader:
                current_program_name = row[program_name_index]
                current_datetime = row[datetime_index]
                current_id = row[id_index]
                if prev_program_name is None: #最初の行でのみ実行
                    prev_program_name = current_program_name
                    prev_datetime = current_datetime
                    prev_id = current_id
                    duration = 1  # 1行目なので1分間の視聴は確定
                elif current_program_name == prev_program_name: # 番組名が同じ -> 視聴時間を累計
                    duration += 1
                else: # 番組名が異なる場合、これまでのデータを出力してリセット
                    csvwriter.writerow([prev_id, prev_datetime, duration])
                    prev_program_name = current_program_name
                    prev_datetime = current_datetime
                    prev_id = current_id
                    duration = 1  # 新しい番組の1分間の視聴が確定
            csvwriter.writerow([prev_id, prev_datetime, duration])

process_tv_csv('../TV.csv', '../data/Formatted_csv/TV_formatted.csv')
