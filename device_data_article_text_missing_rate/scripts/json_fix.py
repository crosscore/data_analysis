import json

def fix_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # JSONオブジェクトを配列に包む
    fixed_lines = [line.strip() for line in lines if line.strip()]
    fixed_json = json.dumps([json.loads(line) for line in fixed_lines], ensure_ascii=False, indent=4)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(fixed_json)

file_path = '../data/csv/original_json/oian4zolsu56pphe5htcdt7pry.json'
fix_json_file(file_path)
