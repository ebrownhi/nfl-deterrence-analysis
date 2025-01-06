import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from diptest import diptest



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

on_ball = week1[week1['alignment_tag'] == 'On Ball']['redirection_percentage']
off_ball = week1[week1['alignment_tag'] == 'Off Ball']['redirection_percentage']

# Perform Shapiro-Wilk test for both
shapiro_on = stats.shapiro(on_ball)
shapiro_off = stats.shapiro(off_ball)

print(f"On-Ball Test Statistic: {shapiro_on.statistic:.4f}, P-value: {shapiro_on.pvalue:.4f}")
print(f"Off-Ball Test Statistic: {shapiro_off.statistic:.4f}, P-value: {shapiro_off.pvalue:.4f}")

# Interpretation
if shapiro_on.pvalue > 0.05:
    print("On-ball redirection rates appear normally distributed.")
else:
    print("On-ball redirection rates are not normally distributed.")

if shapiro_off.pvalue > 0.05:
    print("Off-ball redirection rates appear normally distributed.")
else:
    print("Off-ball redirection rates are not normally distributed.")

dip_value, p_value = diptest(np.array(on_ball))
print(f"Dip Test Statistic: {dip_value:.4f}, p-value: {p_value:.4f}")