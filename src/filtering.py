import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


dtypes = {
    'gameId': 'int32',
    'playId': 'int32',
    'nflId': 'Int32',  # Nullable integer
    'x': 'float32',
    'y': 'float32'
}

# players_dtype = {'nflId': 'int32', 'position': 'category'}

week1 = pd.read_csv('Data/tracking_week_1.csv', dtype=dtypes)
# week1_chunks = pd.read_csv('Data/tracking_week_1.csv', dtype=dtypes, chunksize=500000)
# players = pd.read_csv('Data/players.csv', dtype=players_dtype)

# # player_play = pd.read_csv('Data/player_play.csv')

# plays = pd.read_csv('Data/plays.csv')


# # run this to create the new dataset


# filtered_data = []

# for week1 in week1_chunks:
#     week1.set_index('nflId', inplace=True)


#     # Merge players to get position information
#     week1 = week1.merge(players[['nflId', 'position']], on='nflId', how='left')


#     # Merge relevant play information
#     week1 = week1.join(plays[['playId', 'rushLocationType']], on='playId', how='right', rsuffix='_plays')

#     # Filter for snap data early
#     snap_data = week1[week1['event'] == 'ball_snap']

#     # Filter for run plays and front 7 positions
#     run_plays = snap_data[snap_data['rushLocationType'].notna()]
#     front7_positions = {'OLB', 'NT', 'MLB', 'ILB', 'DE', 'DT', 'LB'}
#     front7_data = run_plays[run_plays['position'].isin(front7_positions)]

#     # Append to filtered list
#     filtered_data.append(front7_data)

# front7_data = pd.concat(filtered_data)

# front7_data.to_csv('data/front7_data.csv', index=False)

# # pass_plays = plays[(plays['isDropback'] == True) | (snap_data['passResult'].notna())]

# # print(f"Number of columns in plays: {len(plays)}")

# # print(f"Number of columns in run_plays: {len(run_plays)}")

# # led to
# # Number of columns in plays: 16124
# # Number of columns in run_plays: 6788

# # positionNameSet = set()   
# # for i in players["position"]:
# #     positionNameSet.add(i)
# # print(positionNameSet)

# # led to
# # {'OLB', 'NT', 'WR', 'CB', 'C', 'MLB', 'FB', 'ILB', 'DE', 'G', 'T', 'DB', 'DT', 'RB', 'FS', 'TE', 'SS', 'QB', 'LB'}

front7_data = pd.read_csv('Data/front7_data.csv')

def create_ball_position_dict(tracking_data):
    ball_data = tracking_data[tracking_data['nflId'].isna()]
    ball_at_snap = ball_data[ball_data['event'] == 'ball_snap']
    return dict(zip(zip(ball_at_snap['gameId'], ball_at_snap['playId']), 
                    zip(ball_at_snap['x'], ball_at_snap['y'])))

ball_position_dict = create_ball_position_dict(week1)

def normalize_coordinates(df, ball_position_dict):
    multi_index = list(zip(df['gameId'], df['playId']))
    ball_positions = pd.DataFrame(
    [ball_position_dict.get(key, (0, 0)) for key in multi_index],  # Ensures order matches
    columns=['ball_x', 'ball_y'],
    index=df.index  # Explicitly match index with df 
    )

    # Vectorized adjustment of x and y coordinates
    df[['x', 'y']] -= ball_positions.values

    # Efficient flipping for leftward plays
    mask = df['playDirection'] == 'left'
    df.loc[mask, ['x', 'y']] *= -1
    
    return df

# Normalize and Create Heatmap
normalized_data = normalize_coordinates(front7_data, ball_position_dict)

alignment_data = normalized_data[['nflId', 'gameId', 'playId', 'x', 'y']]
alignment_data['x_bin'] = pd.cut(alignment_data['x'], bins=50)
alignment_data['y_bin'] = pd.cut(alignment_data['y'], bins=50)

heatmap_data = alignment_data.pivot_table(
    index='y_bin', columns='x_bin', aggfunc='size', fill_value=0
)



plt.figure(figsize=(12, 6))
plt.hist2d(front7_data['x'], front7_data['y'], bins=[50, 30], cmin=1, cmap='YlGnBu')

plt.colorbar(label='Frequency')
plt.xlabel('x (Yards from End Zone)')
plt.ylabel('y (Yards from Sideline)')
plt.title('Defensive Front 7 Alignments Heatmap')

# Adjust axes to reflect NFL field dimensions
plt.xlim(-5, 20)  # Allowing some space for negative x-values
plt.ylim(-15, 15)

plt.xticks(np.arange(-4, 20, 2))  # 10-yard increments for length
plt.yticks(np.arange(-15, 15, 5))  # 5-yard increments for width

plt.grid(True)
plt.show()