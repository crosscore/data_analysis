import pandas as pd

df = pd.read_csv('../../data/csv/soft_and_hard/device_soft_and_hard.csv', dtype={'user': str})

grouping_dict = {'1st_half': [1, 2, 3, 4, 5, 6, 7], '2nd_half': [8, 9, 10, 11, 12, 13, 14]}
print(df)

# Create a mapping from categories to group names by reversing the original dictionary
reverse_dict = {category: group for group, categories in grouping_dict.items() for category in categories}
df['days'] = df['days'].map(reverse_dict)
print(df)

df.to_csv('../../data/csv/1st_half_and_2nd_half/device_1st_half_and_2nd_half.csv', index=False)
print(df['days'].value_counts(dropna=False))