import os
import subprocess

# 現在のディレクトリの全ての.pyファイルを取得
files = [f for f in os.listdir('.') if f.endswith('.py')]

# 各ファイルを順番に実行
for file in files:
    subprocess.run(['python', file])
