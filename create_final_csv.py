import pandas as pd

match_player_data = pd.read_csv('./data/match_player_data.csv')
merged_match_data = pd.read_csv('./data/merged_match_data.csv')

merged_match_data['Home Goal Difference'] = merged_match_data['Home Goals'] - merged_match_data['Away Goals']
merged_match_data['Result'] = merged_match_data['Home Goal Difference'].apply(lambda x: 1 if x > 0 else (0 if x == 0 else -1))

excluded_stats_columns = ['Initial Year', 'Player', 'Minutes Played']
excluded_match_columns = ['Year', 'Home Goals', 'Away Goals', 'Home Goal Difference', 'Result']

final_set = pd.DataFrame()

list_of_stats = []
for col in match_player_data.columns:
    if col not in excluded_stats_columns:
        list_of_stats.append(col)

match_player_data['Initial Year'] = match_player_data['Initial Year'].astype(int)
match_player_data['Player'] = pd.to_numeric(match_player_data['Player'], errors='coerce').fillna(0).astype(int)

match_stats = {}
# Iterate over each match:
for _, row in merged_match_data.iterrows():
    year = int(row['Year'])
    match_id = row['Match ID']
    home_players = []
    away_players = []

    # Filter columns based on the match id
    current_match_rows = merged_match_data[merged_match_data['Match ID'] == match_id]

    # Extract the list of home and away players
    for _, row in current_match_rows.iterrows():
        for col in merged_match_data.columns:
            if 'HomePlayer' in col:
                if pd.isna(row[col]):
                    player_id = 0
                else:
                    player_id = int(row[col])
                home_players.append(player_id)
            elif 'AwayPlayer' in col:
                if pd.isna(row[col]):
                    player_id = 0
                else:
                    player_id = int(row[col])
                away_players.append(player_id)

    print(f'Home players for match {match_id}: {home_players}')
    print(f'Away players for match {match_id}: {away_players}')

    # Calculate the average of each stat per 90 minutes for all home or away players in the current match
    match_stat_totals = {}
    for stat in list_of_stats:
        home_stat_total = 0
        away_stat_total = 0

        for player in home_players:
            filtered_df = match_player_data.loc[(match_player_data['Player'] == player) & (match_player_data['Initial Year'] == year), stat]
            if not filtered_df.empty:
                value = filtered_df.iloc[0]
            else:
                value = 0
            home_stat_total += value
            print(f"Home player {player}, Year {year}, Stat {stat}, Filtered Value: {value}")

        for player in away_players:
            filtered_df = match_player_data.loc[(match_player_data['Player'] == player) & (match_player_data['Initial Year'] == year), stat]
            if not filtered_df.empty:
                value = filtered_df.iloc[0]
            else:
                value = 0
            away_stat_total += value
            print(f"Away player {player}, Year {year}, Stat {stat}, Filtered Value: {value}")


        # Calculate the average per 90 minutes
        home_stat_avg = home_stat_total / len(home_players)
        away_stat_avg = away_stat_total / len(away_players)

        # Append the calculated averages to the final set
        match_stat_totals[f'Average {stat} per 90 Home'] = home_stat_avg
        match_stat_totals[f'Average {stat} per 90 Away'] = away_stat_avg

    print(f'Calculated all stats for match {match_id}.')

    # Calculate match result and home goal difference
    result = row['Result']
    home_goal_difference = row['Home Goal Difference']

    # Store match statistics in the dictionary
    match_stats[match_id] = match_stat_totals
    match_stats[match_id]['Result'] = result
    match_stats[match_id]['Home Goal Difference'] = home_goal_difference

# Create DataFrame from the dictionary
final_set = pd.DataFrame.from_dict(match_stats, orient='index')

# Write DataFrame to CSV
final_set.to_csv('final_dataset.csv')