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
week1 = pd.read_csv('Data/categorized_weeks.csv', dtype=dtypes)

plays = pd.read_csv('Data/plays.csv')

# Merge expectedPoints from plays.csv
week1 = week1.merge(plays[['gameId', 'playId', 'expectedPointsAdded']], on=['gameId', 'playId'], how='left')
def calculate_redirection_percentage(df):
    # Group by player and calculate redirection rate
    redirection_stats = df.groupby('nflId').agg(
        total_plays=('redirected_run', 'count'),
        redirected_plays=('redirected_run', 'sum')
    )
    
    # Calculate percentage
    redirection_stats['redirection_percentage'] = (
        redirection_stats['redirected_plays'] / redirection_stats['total_plays']
    ) * 100

    # Filter for non-redirected plays and calculate mean expectedPoints
    non_redirected_plays = df[df['redirected_run'] == False]
    expected_points_mean = non_redirected_plays.groupby('nflId')['expectedPointsAdded'].mean()

    # Merge the expected points back into the redirection_stats DataFrame
    redirection_stats = redirection_stats.merge(expected_points_mean.rename('expectedPoints'), 
                                                on='nflId', how='left')

    # Assign On Ball or Off Ball tag based on alignment category
    alignment_tag = df.groupby('nflId')['alignment_category'].apply(
        lambda x: 'Off Ball' if (x == 'Left Off Ball').sum() + (x == 'Right Off Ball').sum() > (len(x) / 2) else 'On Ball'
    )

    redirection_stats = redirection_stats.merge(alignment_tag.rename('alignment_tag'), on='nflId')

    # Sort for better visualization
    redirection_stats = redirection_stats.sort_values(by='redirection_percentage', ascending=False)

    return redirection_stats.reset_index()

player_percentage = calculate_redirection_percentage(week1)

player_percentage.to_csv('Data/player_percentage_full.csv', index=False)

print(player_percentage[['nflId', 'total_plays', 'redirected_plays', 'alignment_tag', 'redirection_percentage']].head(20))


