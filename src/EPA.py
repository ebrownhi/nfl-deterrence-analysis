import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from playerp import calculate_redirection_percentage as crp
from sklearn.model_selection import train_test_split

# Load datasets
dtypes = {
    'gameId': 'int32',
    'playId': 'int32',
    'nflId': 'Int32',
    'x': 'float32',
    'y': 'float32'
}

week1 = pd.read_csv('Data/categorized_weeks.csv', dtype=dtypes)

plays = pd.read_csv('Data/plays.csv')

# Merge expectedPoints from plays.csv
week1 = week1.merge(plays[['gameId', 'playId', 'expectedPointsAdded']], on=['gameId', 'playId'], how='left')

# Step 1: Filter for Weeks 1-5 and 6-9
week1['gameId'] = pd.to_numeric(week1['gameId'], errors='coerce')
weeks_1_5 = week1[week1['gameId'] <= 2022101000]
weeks_6_9 = week1[week1['gameId'] > 2022101000]

# Step 2: Calculate redirection percentage, including expectedPoints in the grouped output
weeks_1_5 = crp(weeks_1_5)
weeks_6_9 = crp(weeks_6_9)

# Step 3: Calculate average redirection% and expectedPoints by player
redirection_1_5 = weeks_1_5.groupby('nflId', as_index=False).agg({
    'redirection_percentage': 'mean',
    'expectedPoints': 'mean',
    'total_plays': 'sum',
    'alignment_tag': 'first'
})

redirection_6_9 = weeks_6_9.groupby('nflId', as_index=False).agg({
    'redirection_percentage': 'mean',
    'expectedPoints': 'mean',
    'total_plays': 'sum',
    'alignment_tag': 'first'
})

# Merge dataframes on player ID
combined_data = pd.merge(redirection_1_5, redirection_6_9, on='nflId', suffixes=('_1_5', '_6_9'))


# Filter players with sufficient plays
min_plays = 30
combined_data = combined_data[(combined_data['total_plays_1_5'] + 
                               combined_data['total_plays_6_9']) >= min_plays]

# Fill NaN values with the mean of expectedPoints
combined_data['expectedPoints_6_9'].fillna(combined_data['expectedPoints_6_9'].mean(), inplace=True)


# Step 4: Regression Analysis (Redirection% vs Expected Points)
X = combined_data[['redirection_percentage_1_5']]
y = combined_data['expectedPoints_6_9']

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# Step 5: Evaluate the Model
r2 = r2_score(y, y_pred)
print(f'R-squared for Redirection% and Expected Points: {r2:.4f}')

# Step 6: Plot Results
plt.figure(figsize=(8, 6))
plt.scatter(X, y, color='blue', label='Actual Data')
plt.plot(X, y_pred, color='red', label='Regression Line')
plt.xlabel('Redirection% (Weeks 1-5)')
plt.ylabel('Expected Points (Weeks 6-9)')
plt.title('Correlation between Redirection% and Expected Points')
plt.legend()
plt.show()
