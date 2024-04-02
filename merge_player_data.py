import os
import pandas as pd

data_folder_path = './player_statistics'

dfs = []

# Combine all player individual statistics into a single CSV

for file_name in os.listdir(data_folder_path):
    if file_name.endswith('.csv'):
        # Construct the file path
        file_path = os.path.join(data_folder_path, file_name)
        
        # Load the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Drop irrelevant columns
        df = df.drop(columns=['Rank', 'Club', 'Nationality'], errors='ignore')
        
        # Rename the 'Stat' column to the name of the file
        new_stat_column_name = os.path.splitext(file_name)[0]
        df.rename(columns={'Stat': new_stat_column_name}, inplace=True)
        
        # Append the DataFrame to the list
        dfs.append(df)

merged_df = dfs[0]

for df in dfs[1:]:
    merged_df = pd.merge(merged_df, df, on=['Initial Year', 'Player'], how='outer')

merged_df = merged_df.drop_duplicates(subset=['Initial Year', 'Player'])

excluded_columns = ['Initial Year', 'Player']
for col in merged_df.columns:
    if col not in excluded_columns:
        merged_df[col] = merged_df[col].astype(str).str.replace('"', '')
        merged_df[col] = merged_df[col].str.replace(',', '').astype(float)

mean_minutes_played = merged_df['Minutes Played'].mean()
merged_df['Minutes Played'] = merged_df['Minutes Played'].fillna(mean_minutes_played)

merged_df.fillna(0, inplace=True)

excluded_columns = ['Initial Year', 'Player', 'Minutes Played']
for col in merged_df.columns:
    if col not in excluded_columns:
        merged_df[col] = merged_df[col] / merged_df['Minutes Played']

merged_df.to_csv('./data/merged_player_data.csv', index=False)

