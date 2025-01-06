import pandas as pd

# Load the CSV file
games = pd.read_csv('Data/games.csv')

# Convert gameId to numeric (in case it's not)
games['gameId'] = pd.to_numeric(games['gameId'], errors='coerce')
games['week'] = pd.to_numeric(games['week'], errors='coerce')


# Filter for games that fall after week 5 (weeks 6-9)
filtered_games = games[games['gameId'] > 2022101000]

# Check if all gameIds are greater than the threshold
if (filtered_games['week'] > 5).all():
    print("All gameIds for weeks 6-9 are greater than 2022101000.")
else:
    print("Some gameIds for weeks 6-9 are NOT greater than 2022101000.")
    print(filtered_games[filtered_games['gameId'] <= 2022101000])
