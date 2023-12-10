import pandas as pd

df = pd.read_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time.csv', dtype={'user': str})

grouping_dict = {'hard_news': ['国内', '国際', '経済'], 'soft_news': ['エンタメ', 'スポーツ', '地域', 'ライフ', 'IT', '科学']}
print(df)

# Create a mapping from categories to group names by reversing the original dictionary
reverse_dict = {category: group for group, categories in grouping_dict.items() for category in categories}
df['category'] = df['category'].map(reverse_dict)
print(df)

df.to_csv('../../data/csv/add_viewing_time/device_add_days_viewing_time_soft_hard.csv', index=False)