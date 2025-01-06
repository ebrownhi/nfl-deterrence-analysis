import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# helps pandas load
dtypes = {
    'gameId': 'int32',
    'playId': 'int32',
    'nflId': 'Int32',  # Nullable integer
    'x': 'float32',
    'y': 'float32'
}
players_dtype = {'nflId': 'int32', 'position': 'category'}

# load data from datasets
week1_chunks = pd.read_csv('Data/tracking_week_1.csv', dtype=dtypes, chunksize=500000)
players = pd.read_csv('Data/players.csv', dtype=players_dtype)
# player_play = pd.read_csv('Data/player_play.csv')
plays = pd.read_csv('Data/plays.csv')

# run this to create the new dataset
filtered_data = []

for week1 in week1_chunks:
    week1.set_index('nflId', inplace=True)


    # Merge players to get position information
    week1 = week1.merge(players[['nflId', 'position']], on='nflId', how='left')


    # Merge relevant play information
    week1 = week1.join(plays[['playId', 'rushLocationType']], on='playId', how='right', rsuffix='_plays')

    # Filter for snap data early
    snap_data = week1[week1['event'] == 'ball_snap']

    # Filter for run plays and front 7 positions
    run_plays = snap_data[snap_data['rushLocationType'].notna()]
    front7_positions = {'OLB', 'NT', 'MLB', 'ILB', 'DE', 'DT', 'LB'}
    front7_data = run_plays[run_plays['position'].isin(front7_positions)]

    # Append to filtered list
    filtered_data.append(front7_data)

# make it into a csv
front7_data = pd.concat(filtered_data)
front7_data.to_csv('data/front7_data.csv', index=False)

# pass_plays = plays[(plays['isDropback'] == True) | (snap_data['passResult'].notna())]

# print(f"Number of columns in plays: {len(plays)}")

# print(f"Number of columns in run_plays: {len(run_plays)}")

# led to
# Number of columns in plays: 16124
# Number of columns in run_plays: 6788

# positionNameSet = set()   
# for i in players["position"]:
#     positionNameSet.add(i)
# print(positionNameSet)

# led to
# {'OLB', 'NT', 'WR', 'CB', 'C', 'MLB', 'FB', 'ILB', 'DE', 'G', 'T', 'DB', 'DT', 'RB', 'FS', 'TE', 'SS', 'QB', 'LB'}

