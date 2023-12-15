import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def plot_histogram(df, file_name, title):
    # Histogram settings
    plt.figure(figsize=(10, 6))
    plt.hist(df['duration'], bins=50, color='skyblue', edgecolor='black')

    # Set graph title and axis labels
    plt.title(title)
    plt.xlabel('Duration')
    plt.ylabel('Frequency')

    # Output path for the PNG file
    output_path = f'../../data/img/histogram/{file_name}'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f'{output_path} has been printed.')

def remove_outliers_by_IQR(df, column):
    # Calculate the first and third quartiles
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Define outlier conditions
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # Identify and return outliers
    outliers_df = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    # Filter out outliers
    filtered_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return filtered_df, outliers_df

def standardize_date_format(df):
    # Convert 'date' column to datetime object
    df['date'] = pd.to_datetime(df['date'])
    # Format it with seconds using apply method
    df['date'] = df['date'].apply(lambda x: x.strftime('%Y/%m/%d %H:%M:%S'))
    return df

# Function to add 'days' column (Experiment period 2 only)
def add_days_to_df(df):
    date_ranges = {
        '0765': ('2022-11-23', '2022-12-06'),
        '0816': ('2022-11-22', '2022-12-05'),
        '1143': ('2022-11-26', '2022-12-09'),
        '2387': ('2022-11-18', '2022-12-05'),
        '2457': ('2022-11-22', '2022-12-05'),
        '3613': ('2022-11-19', '2022-12-02'),
        '3828': ('2022-11-18', '2022-12-01'),
        '4545': ('2022-11-15', '2022-11-28'),
        '4703': ('2022-11-27', '2022-12-10'),
        '5711': ('2022-11-28', '2022-12-11'),
        '5833': ('2022-11-28', '2022-12-11'),
        '6420': ('2022-11-25', '2022-12-08'),
        '7471': ('2022-11-23', '2022-12-06'),
        '8058': ('2022-11-26', '2022-12-09'),
        '9556': ('2022-11-24', '2022-12-07'),
    }
    exclusion_date_user2387 = ['2022-11-20', '2022-11-21', '2022-11-22', '2022-11-23']
    exclusion_dates = pd.to_datetime(exclusion_date_user2387)

    # Exclude certain dates for user '2387'
    for date in exclusion_date_user2387:
        df = df[~((df['user'] == '2387') & df['date'].str.contains(date))]

    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by=['user', 'date'], ascending=[True, True], inplace=True)

    # Delete data outside date_ranges
    for user, (start, end) in date_ranges.items():
        end_date = pd.Timestamp(end) + timedelta(days=1)
        df = df[~((df['user'] == user) & ((df['date'] < pd.Timestamp(start)) | (df['date'] >= end_date)))]

    # Function to calculate days
    def calculate_days(row):
        user = row['user']
        date = row['date']
        start_date = pd.Timestamp(date_ranges[user][0])
        if user == '2387':
            excluded_days_count = sum([1 for excl_date in exclusion_dates if start_date <= excl_date <= date])
            return (date - start_date).days + 1 - excluded_days_count
        else:
            return (date - start_date).days + 1

    df['days'] = df.apply(calculate_days, axis=1)
    return df

df_MobileApp = pd.read_csv("../../data/csv/original/MobileApp.csv", dtype={'user': str})
df_TV = pd.read_csv("../../data/csv/original/TV.csv", dtype={'user': str})

df_MobileApp = df_MobileApp[['user', 'date', 'duration', 'app_category']]
df_TV = df_TV[['user', 'date', 'duration', 'tv_category']]

df_MobileApp = standardize_date_format(df_MobileApp)
df_TV = standardize_date_format(df_TV)

plot_histogram(df_MobileApp, 'before/MobileApp_duration_histogram.png', 'MobileApp Duration Histogram')
plot_histogram(df_TV, 'before/TV_duration_histogram.png', 'TV Duration Histogram')

df_MobileApp_filtered, df_MobileApp_outliers  = remove_outliers_by_IQR(df_MobileApp, 'duration')
df_TV_filtered, df_TV_outliers  = remove_outliers_by_IQR(df_TV, 'duration')

plot_histogram(df_MobileApp_filtered, 'after/MobileApp_duration_histogram.png', 'MobileApp Duration Histogram')
plot_histogram(df_TV_filtered, 'after/TV_duration_histogram.png', 'TV Duration Histogram')

# Add a new column 'source_name' to each dataframe and set its value
df_MobileApp_filtered['source_name'] = 'MobileApp'
df_TV_filtered['source_name'] = 'TV'

# Combine all filtered dataframes into one
combined_filtered_df = pd.concat([
    df_MobileApp_filtered,
    df_TV_filtered
])

# Exclude negative values of duratoin
combined_filtered_df = combined_filtered_df[combined_filtered_df['duration'] >= 0]

# Export combined dataframe to CSV
combined_filtered_df.to_csv('../../data/csv/concat_and_IQR/MBapp_TV_with_category.csv', index=False)

# Repeat the process for outliers dataframes
df_MobileApp_outliers['source_name'] = 'MobileApp'
df_TV_outliers['source_name'] = 'TV'

# Combine all outliers dataframes into one
combined_outliers_df = pd.concat([
    df_MobileApp_outliers,
    df_TV_outliers
])

# Exclude negative values of duratoin
combined_outliers_df = combined_outliers_df[combined_outliers_df['duration'] >= 0]

# Export combined dataframe to CSV
combined_outliers_df.to_csv('../../data/csv/concat_and_IQR/MBapp_TV_with_category_outliers.csv', index=False)
