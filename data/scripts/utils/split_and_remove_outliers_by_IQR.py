import pandas as pd

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

df = pd.read_csv("../../csv/mobile/original/TV_APP/TV_APP.csv", dtype={'user': str})

# Separate into TV viewing data and app usage data
df_tv = df[df['tv_category'].notna()]
df_app = df[df['app_category'].notna()]

# Function to apply IQR
def remove_outliers_by_IQR(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    filtered_df = df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
    return filtered_df

# Apply IQR to each dataset
df_tv_filtered = remove_outliers_by_IQR(df_tv, 'duration')
df_app_filtered = remove_outliers_by_IQR(df_app, 'duration')

# Save results to CSV file
df_tv_filtered.to_csv("../../csv/mobile/original/TV_APP/TV_filtered.csv", index=False)
df_app_filtered.to_csv("../../csv/mobile/original/TV_APP/APP_filtered.csv", index=False)
