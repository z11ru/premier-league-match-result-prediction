import json
import csv

input_file_path = './match_statistics/matches.jsonl'
output_file_path = './data/merged_match_data.csv'

with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    
    headers = ['Match ID', 'Year', 'Home Goals', 'Away Goals'] + \
              [f'HomePlayer{i+1}' for i in range(18)] + \
              [f'AwayPlayer{i+1}' for i in range(18)]
    csv_writer.writerow(headers)
    
    for line in input_file:

        if not line.strip():
            continue
        
        try:
            data = json.loads(line.strip())
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for line: {line}")
            continue
        
        if data['league'] == 'en':
            year = data['season'][:4]
            id = data['match_id']

            home_goals = data['home_score']
            away_goals = data['away_score']
            
            home_players = data['home_starting_players'][:11] + [None]*(11 - len(data['home_starting_players'][:11]))
            away_players = data['away_starting_players'][:11] + [None]*(11 - len(data['away_starting_players'][:11]))

            home_subs = data['home_sub_players'][:7] + [None]*(7 - len(data['home_sub_players'][:7]))
            away_subs = data['away_sub_players'][:7] + [None]*(7 - len(data['away_sub_players'][:7]))
            
            row = [id, year, home_goals, away_goals] + home_players + home_subs + away_players + away_subs
            csv_writer.writerow(row)
