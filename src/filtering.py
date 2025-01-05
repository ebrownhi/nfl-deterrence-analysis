import pandas as pd

player_play = pd.read_csv('path_to/player_play.csv')

plays = pd.read_csv('path_to/plays.csv')

run_plays = plays[plays['rushLocationType'].notna()]

pass_plays = plays[(plays['isDropback'] == True) | (plays['passResult'].notna())]
