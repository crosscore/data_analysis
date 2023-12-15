import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def plot_histogram(df, file_name, title):
    # Histogram settings
    plt.figure(figsize=(10, 6))
    plt.hist(df['duration'], bins=30, color='skyblue', edgecolor='black')

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

def filter_dates(df):
    exp1_range = ['2022-10-22', '2022-11-04']
    exp1_range = ['2022-10-22', '2022-11-04']
    exp2_ranges = {
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
    exclusion_dates_2387 = pd.to_datetime(exclusion_date_user2387)

    df['date'] = pd.to_datetime(df['date'])
    filtered_dfs = [] 

    df_exp1 = df[df['date'].between(*pd.to_datetime(exp1_range))]
    filtered_dfs.append(df_exp1)

    for user, (start_date, end_date) in exp2_ranges.items():
        df_user = df[df['user'] == user]
        if user == '2387':
            df_user = df_user[~df_user['date'].isin(exclusion_dates_2387)]
        df_user = df_user[df_user['date'].between(pd.to_datetime(start_date), pd.to_datetime(end_date))]
        filtered_dfs.append(df_user)
    filtered_df = pd.concat(filtered_dfs)
    return filtered_df

df_MobileApp = pd.read_csv("../../data/csv/original/MobileApp.csv", dtype={'user': str})
df_MobileWeb = pd.read_csv("../../data/csv/original/MobileWeb.csv", dtype={'user': str})
df_PC = pd.read_csv("../../data/csv/original/PC.csv", dtype={'user': str})
df_TV = pd.read_csv("../../data/csv/original/TV.csv", dtype={'user': str})

df_MobileApp = df_MobileApp[['user', 'date', 'duration']]
df_MobileWeb = df_MobileWeb[['user', 'date', 'duration']]
df_PC = df_PC[['user', 'date', 'duration']]
df_TV = df_TV[['user', 'date', 'duration']]

df_MobileApp = standardize_date_format(df_MobileApp)
df_MobileWeb = standardize_date_format(df_MobileWeb)
df_PC = standardize_date_format(df_PC)
df_TV = standardize_date_format(df_TV)

df_MobileApp = filter_dates(df_MobileApp)
df_MobileWeb = filter_dates(df_MobileWeb)
df_PC = filter_dates(df_PC)
df_TV = filter_dates(df_TV)

plot_histogram(df_MobileApp, 'before/MobileApp_duration_histogram.png', 'MobileApp Duration Histogram')
plot_histogram(df_MobileWeb, 'before/MobileWeb_duration_histogram.png', 'MobileWeb Duration Histogram')
plot_histogram(df_PC, 'before/PC_duration_histogram.png', 'PC Duration Histogram')
plot_histogram(df_TV, 'before/TV_duration_histogram.png', 'TV Duration Histogram')

df_MobileApp_filtered, df_MobileApp_outliers  = remove_outliers_by_IQR(df_MobileApp, 'duration')
df_MobileWeb_filtered, df_MobileWeb_outliers  = remove_outliers_by_IQR(df_MobileWeb, 'duration')
df_PC_filtered, df_PC_outliers  = remove_outliers_by_IQR(df_PC, 'duration')
df_TV_filtered, df_TV_outliers  = remove_outliers_by_IQR(df_TV, 'duration')

plot_histogram(df_MobileApp_filtered, 'after/MobileApp_duration_histogram.png', 'MobileApp Duration Histogram')
plot_histogram(df_MobileWeb_filtered, 'after/MobileWeb_duration_histogram.png', 'MobileWeb Duration Histogram')
plot_histogram(df_PC_filtered, 'after/PC_duration_histogram.png', 'PC Duration Histogram')
plot_histogram(df_TV_filtered, 'after/TV_duration_histogram.png', 'TV Duration Histogram')

# Add a new column 'source_name' to each dataframe and set its value
df_MobileApp_filtered['source_name'] = 'MobileApp'
df_MobileWeb_filtered['source_name'] = 'MobileWeb'
df_PC_filtered['source_name'] = 'PC'
df_TV_filtered['source_name'] = 'TV'

# Combine all filtered dataframes into one
combined_filtered_df = pd.concat([
    df_MobileApp_filtered,
    df_MobileWeb_filtered,
    df_PC_filtered,
    df_TV_filtered
])

# Exclude negative values of duratoin
combined_filtered_df = combined_filtered_df[combined_filtered_df['duration'] >= 0]

# Export combined dataframe to CSV
combined_filtered_df.to_csv('../../data/csv/concat_and_IQR/MBapp_MBweb_PC_TV.csv', index=False)

# Repeat the process for outliers dataframes
df_MobileApp_outliers['source_name'] = 'MobileApp'
df_MobileWeb_outliers['source_name'] = 'MobileWeb'
df_PC_outliers['source_name'] = 'PC'
df_TV_outliers['source_name'] = 'TV'

# Combine all outliers dataframes into one
combined_outliers_df = pd.concat([
    df_MobileApp_outliers,
    df_MobileWeb_outliers,
    df_PC_outliers,
    df_TV_outliers
])

# Exclude negative values of duratoin
combined_outliers_df = combined_outliers_df[combined_outliers_df['duration'] >= 0]

# Export combined dataframe to CSV
combined_outliers_df.to_csv('../../data/csv/concat_and_IQR/MBapp_MBweb_PC_TV_outliers.csv', index=False)
