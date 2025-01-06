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
week1 = pd.read_csv('Data/normalized_weeks.csv', dtype=dtypes)

# Categorize player alignments
def categorize_player_alignment(df):


    conditions = [
        (df['x'] < 3) & (df['y'] > 3),   # Right Edge
        (df['x'] < 3) & (df['y'] <= 3) & (df['y'] > 0),  # Right Inside
        (df['x'] < 3) & (df['y'] >= -3) & (df['y'] <= 0),  # Left Inside
        (df['x'] < 3) & (df['y'] < -3),   # Left Edge
        (df['x'] >=3 ) & (df['y'] < 0 ),  # Right Off Ball
        (df['x'] >=3) & (df['y'] > 0)   # Left Off Ball
    ]
    
    choices = [
        'Right Edge', 
        'Right Inside', 
        'Left Inside', 
        'Left Edge', 
        'Right Off Ball', 
        'Left Off Ball'
    ]
    
    df['alignment_category'] = np.select(conditions, choices, default='Unclassified')
    
    return df

# Apply categorization
normalized_data = categorize_player_alignment(week1)

normalized_data = normalized_data[normalized_data['alignment_category'] != 'Unclassified']
normalized_data = normalized_data[normalized_data['rushLocationType'] != 'UNKNOWN']

# Evaluate redirection logic
def evaluate_run_redirection(df):

    # Check if defensive line players redirected the run
    df['redirected_run'] = True
    defensive_line = df['alignment_category'].isin(['Left Edge', 'Left Inside', 'Right Inside', 'Right Edge'])

    rush_pairs = {
        'Left Edge' : "OUTSIDE_RIGHT",
        'Right Edge' : "OUTSIDE_LEFT",
        'Left Inside' : "INSIDE_RIGHT",
        'Right Inside' : "INSIDE_LEFT",
        'Right Off Ball': "LEFT",
        'Left Off Ball': "RIGHT"
    }

    # Direct comparison for defensive line players
    df.loc[defensive_line, 'redirected_run'] = (
    df['alignment_category'].map(rush_pairs) != df['rushLocationType'])

    # For off-ball players, only check left/right alignment
    off_ball = df['alignment_category'].isin(['Left Off Ball', 'Right Off Ball'])
    
    df.loc[off_ball, 'redirected_run'] = (
    ~df['alignment_category'].map(rush_pairs).isin(df['rushLocationType']))

    return df

# Apply redirection evaluation
normalized_data = evaluate_run_redirection(normalized_data)

# Save the results
normalized_data.to_csv('data/categorized_weeks.csv', index=False)

# Display sample results
print(normalized_data[['gameId', 'playId', 'nflId', 'x', 'y', 'alignment_category', 'redirected_run']].head(20))
