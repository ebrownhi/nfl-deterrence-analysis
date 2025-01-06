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
week1raw = pd.read_csv('Data/player_percentage_full.csv', dtype=dtypes)

# Filter by minimum plays
min_plays = 30  # Set the minimum number of plays
week1 = week1raw[week1raw['total_plays'] >= min_plays]

off_ball_df = week1[week1['alignment_tag'] == 'Off Ball']
on_ball_df = week1[week1['alignment_tag'] == 'On Ball']
print(off_ball_df.head(10))

# Plotting
# Bin the redirection percentage into 50 bins
week1 = off_ball_df
week1['binned_redirection'] = pd.cut(week1['redirection_percentage'], bins=50)

# Count the frequency of each bin
redirection_counts = week1['binned_redirection'].value_counts().sort_index()

# Plotting
plt.figure(figsize=(12, 6))
plt.bar(redirection_counts.index.astype(str), redirection_counts.values, color='skyblue', edgecolor='black')
plt.title('Off Ball Redirection Rate Distribution (min 50 plays)')
plt.xlabel('Redirection Rate')
plt.ylabel('Frequency')

# Shorten the bin labels by formatting them
bin_labels = [f"{int(bin.left)}-{int(bin.right)}" for bin in redirection_counts.index]
plt.xticks(ticks=range(len(bin_labels)), labels=bin_labels, rotation=45)

plt.grid(axis='y', alpha=0.5)
plt.show()

# Plotting
# Bin the redirection percentage into 50 bins
week1 = on_ball_df
week1['binned_redirection'] = pd.cut(week1['redirection_percentage'], bins=50)

# Count the frequency of each bin
redirection_counts = week1['binned_redirection'].value_counts().sort_index()

# Plotting
plt.figure(figsize=(12, 6))
plt.bar(redirection_counts.index.astype(str), redirection_counts.values, color='skyblue', edgecolor='black')
plt.title('On Ball Redirection Rate Distribution (min 50 plays)')
plt.xlabel('Redirection Rate')
plt.ylabel('Frequency')

# Shorten the bin labels by formatting them
bin_labels = [f"{int(bin.left)}-{int(bin.right)}" for bin in redirection_counts.index]
plt.xticks(ticks=range(len(bin_labels)), labels=bin_labels, rotation=45)

plt.grid(axis='y', alpha=0.5)
plt.show()

