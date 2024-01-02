import pandas as pd

df = pd.read_csv('TV_original.csv', dtype={'user': str})

current_user = None
current_program = None
current_duration = 0
first_row = None

output_data = []
for index, row in df.iterrows():
    # When the user or program name changes, or when the sequence ends
    if current_user != row['user'] or current_program != row['program_name']:
        if current_user is not None:
            # update duration and add to list
            first_row['duration'] = current_duration
            output_data.append(first_row)
        # Start program sequence with new user
        current_user = row['user']
        current_program = row['program_name']
        current_duration = 0
        first_row = row
    # increase duration
    current_duration += 60

# add last sequence
if current_user is not None:
    first_row['duration'] = current_duration
    output_data.append(first_row)

output_df = pd.DataFrame(output_data)
output_df.sort_values(by=['user', 'date'], inplace=True)
output_df.reset_index(drop=True, inplace=True)
output_df.to_csv('TV.csv', index=False)
print(output_df)
