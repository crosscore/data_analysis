import pandas as pd
import glob

csv_files = glob.glob("../csv_original_files/mobile/warehouse/*.csv")

for file in csv_files:
    df = pd.read_csv(file)
    df['user'] = df['user'].astype(str).str.zfill(4)
    df.to_csv(file.replace(".csv", "_fix.csv"), index=False)