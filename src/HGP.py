import pandas as pd
import matplotlib.pyplot as plt

# Load the data
normalized_data = pd.read_csv('Data/normalized_wk1.csv')

# Filter data
on_line_players = normalized_data[normalized_data['x'] < 3]
off_ball_players = normalized_data[normalized_data['x'] > 3]

# Plot for on-line players
plt.figure(figsize=(10, 6))
plt.hist(on_line_players['y'], bins=250, color='skyblue', edgecolor='black')
plt.title('Distribution of Horizontal Distance - On Line Players (x < 3)')
plt.xlabel('Horizontal distance (negative is left)')
plt.ylabel('Frequency')
plt.xlim(-10, 10)
plt.grid(axis='y', alpha=0.75)
plt.show()

# Plot for off-ball players
plt.figure(figsize=(10, 6))
plt.hist(off_ball_players['y'], bins=250, color='orange', edgecolor='black')
plt.title('Distribution of Horizontal Distance - Off Ball Players (x > 3)')
plt.xlabel('Horizontal distance (negative is left)')
plt.ylabel('Frequency')
plt.xlim(-10, 10)
plt.grid(axis='y', alpha=0.75)
plt.show()
