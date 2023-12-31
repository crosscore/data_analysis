import os
import subprocess
from tqdm import tqdm

directory = '../normal/'

# Get all .py files from directory and its subdirectories
files = []
for dirpath, dirnames, filenames in os.walk(directory):
    # Exclude utils directory if it exists
    if 'utils' in dirnames:
        dirnames.remove('utils')
    for file in filenames:
        if file.endswith('.py'):
            files.append(os.path.join(dirpath, file))

for file in tqdm(files):
    try:
        print(f'excute: {file}')
        subprocess.run(['python', file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"エラー: {file} の実行中に問題が発生しました: {e}")
