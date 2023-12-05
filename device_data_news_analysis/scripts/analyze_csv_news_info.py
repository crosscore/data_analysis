import pandas as pd

df = pd.read_csv("../data/csv/all_user_plus_json.csv", dtype={'user': str})
print(df.head())

print(df.info())

print('---------')
print(f'df.isnull().sum():\n{df.isnull().sum()}')
print('---------')
print(f'df.describe():\n{df.describe()}')
print('---------')
print(f"df[df['article_url'].duplicated()]['article_url']:\n{df[df['article_url'].duplicated()]['article_url']}")
print('---------')
for column in df.columns:
    print(f"{column}の重複数: {df[column].duplicated().sum()}")