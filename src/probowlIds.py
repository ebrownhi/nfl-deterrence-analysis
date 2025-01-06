import pandas as pd
from scipy import stats


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

pro_bowlers = pd.read_csv('Data/ProBowlers.csv')
players = pd.read_csv('Data/players.csv')

# Rename the 'Player' column to 'displayName' to match players.csv
pro_bowlers.rename(columns={'Player': 'displayName'}, inplace=True)

merged = pro_bowlers.merge(players, on=['displayName'], how='inner')
pro_bowler_ids = merged[['nflId', 'displayName']]
pro_bowler_redirection = week1.merge(pro_bowler_ids, on='nflId', how='inner')

# Filter by alignment (assuming 'alignment_tag' exists in redirection_data)
on_ball = week1[week1['alignment_tag'] == 'On Ball']
off_ball = week1[week1['alignment_tag'] == 'Off Ball']

pro_on_ball = pro_bowler_redirection[pro_bowler_redirection['alignment_tag'] == 'On Ball']
pro_off_ball = pro_bowler_redirection[pro_bowler_redirection['alignment_tag'] == 'Off Ball']

# Calculate league averages
league_on_avg = on_ball['redirection_percentage'].mean()
league_off_avg = off_ball['redirection_percentage'].mean()

# Calculate Pro Bowler averages
pro_on_avg = pro_on_ball['redirection_percentage'].mean()
pro_off_avg = pro_off_ball['redirection_percentage'].mean()

print(f"League Average On-Ball Redirection%: {league_on_avg:.2f}%")
print(f"League Average Off-Ball Redirection%: {league_off_avg:.2f}%")

print(f"Pro Bowler Average On-Ball Redirection%: {pro_on_avg:.2f}%")
print(f"Pro Bowler Average Off-Ball Redirection%: {pro_off_avg:.2f}%")


# Extract redirection percentages for Off-Ball Pro Bowlers and Full NFL
pro_off_ball_redirection = pro_off_ball['redirection_percentage'].dropna()
off_ball_redirection = off_ball['redirection_percentage'].dropna()

# ANOVA for Off-Ball Players (Pro Bowl vs Full NFL)
f_stat_off, p_value_off = stats.f_oneway(pro_off_ball_redirection, off_ball_redirection)
print(f"Off-Ball ANOVA F-statistic: {f_stat_off:.2f}")
print(f"Off-Ball ANOVA p-value: {p_value_off:.4f}")

if p_value_off < 0.05:
    print("Statistically significant difference between Pro Bowl and full NFL off-ball players.")
else:
    print("No significant difference between Pro Bowl and full NFL off-ball players.")

# Extract redirection percentages for On-Ball Pro Bowlers and Full NFL
pro_on_ball_redirection = pro_on_ball['redirection_percentage'].dropna()
on_ball_redirection = on_ball['redirection_percentage'].dropna()

# ANOVA for On-Ball Players (Pro Bowl vs Full NFL)
f_stat_on, p_value_on = stats.f_oneway(pro_on_ball_redirection, on_ball_redirection)
print(f"\nOn-Ball ANOVA F-statistic: {f_stat_on:.2f}")
print(f"On-Ball ANOVA p-value: {p_value_on:.4f}")

if p_value_on < 0.05:
    print("Statistically significant difference between Pro Bowl and full NFL on-ball players.")
else:
    print("No significant difference between Pro Bowl and full NFL on-ball players.")



