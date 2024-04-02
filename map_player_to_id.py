import pandas as pd

player_ids_df = pd.read_csv('./match_statistics/players.csv', sep='|')
player_ids_df['nickname'] = player_ids_df['nickname'].fillna('')

name_to_id_mapping = {}
for _, row in player_ids_df.iterrows():
    full_name = f"{row['first_name']} {row['last_name']}".strip()
    nickname = row['nickname'].strip()
    player_id = row['id']
    name_to_id_mapping[full_name] = player_id
    if nickname:
        name_to_id_mapping[nickname] = player_id

player_data_df = pd.read_csv('./data/merged_player_data.csv')

player_data_df = player_data_df.loc[player_data_df['Initial Year'].between(2017, 2021)]
player_data_df['Player'] = player_data_df['Player'].apply(lambda name: name_to_id_mapping.get(name, name))

player_data_df.to_csv('./data/match_player_data.csv', index=False)
