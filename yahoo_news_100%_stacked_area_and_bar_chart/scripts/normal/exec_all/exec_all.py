import os
import subprocess
from tqdm import tqdm

directory = '../'

# directoryとそのサブディレクトリから全ての.pyファイルを取得
files = []
for dirpath, dirnames, filenames in os.walk(directory):
    if 'exec_all' in dirnames:
        dirnames.remove('exec_all')
    for file in filenames:
        if file.endswith('.py'):
            files.append(os.path.join(dirpath, file))

for file in tqdm(files):
    try:
        print(f'excute: {file}')
        subprocess.run(['python', file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"エラー: {file} の実行中に問題が発生しました: {e}")
