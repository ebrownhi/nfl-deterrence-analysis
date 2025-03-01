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
# load dataset
tracking_data = pd.DataFrame()
for i in range(1, 10):
    week = pd.read_csv(f'Data/tracking_week_{i}.csv', dtype=dtypes)
    tracking_data = pd.concat([tracking_data, week], ignore_index=True)

# dataset created from week 1 tracking values
front7_data = pd.read_csv('Data/front7_data.csv')

# dictionary of ball position by game and play
def create_ball_position_dict(tracking_data):
    ball_data = tracking_data[tracking_data['nflId'].isna()]
    ball_at_snap = ball_data[ball_data['event'] == 'ball_snap']
    return dict(zip(zip(ball_at_snap['gameId'], ball_at_snap['playId']), 
                    zip(ball_at_snap['x'], ball_at_snap['y'])))

ball_position_dict = create_ball_position_dict(tracking_data)

# function that subtracts the play's ball coordinates from the player
def normalize_coordinates(df, ball_position_dict):
    multi_index = list(zip(df['gameId'], df['playId']))
    ball_positions = pd.DataFrame(
    [ball_position_dict.get(key, (0, 0)) for key in multi_index],  # Ensures order matches
    columns=['ball_x', 'ball_y'],
    index=df.index  # Explicitly match index with df 
    )

    # Vectorized adjustment of x and y coordinates
    df[['x', 'y']] -= ball_positions.values

    # Efficient flipping for rightward plays
    mask = df['playDirection'] == 'left'
    df.loc[mask, ['x', 'y']] *= -1
    return df

# Normalize and Create Heatmap
normalized_data = normalize_coordinates(front7_data, ball_position_dict)

normalized_data.to_csv('data/normalized_weeks.csv', index=False)

# binning the data
alignment_data = normalized_data[['nflId', 'gameId', 'playId', 'x', 'y']]
alignment_data['x_bin'] = pd.cut(alignment_data['x'], bins=50)
alignment_data['y_bin'] = pd.cut(alignment_data['y'], bins=50)

heatmap_data = alignment_data.pivot_table(
    index='y_bin', columns='x_bin', aggfunc='size', fill_value=0
)

# plot feature adjustments
plt.figure(figsize=(12, 6))
plt.hist2d(front7_data['x'], front7_data['y'], bins=[100, 60], cmin=1, cmap='YlGnBu')

plt.colorbar(label='Frequency')
plt.xlabel('X (Yards back from the Ball)')
plt.ylabel('Y (Yards horizontal to the Ball (Right is positive))')
plt.title('Defensive Front 7 Alignments Heatmap')

# Adjust axes to reflect NFL field dimensions
plt.xlim(0, 20)  # Allowing some space for negative x-values
plt.ylim(-15, 15)

plt.xticks(np.arange(-0, 20, 2))  # 10-yard increments for length
plt.yticks(np.arange(-15, 15, 5))  # 5-yard increments for width

plt.grid(True)
plt.show()