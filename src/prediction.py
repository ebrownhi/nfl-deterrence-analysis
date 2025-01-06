import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from playerp import calculate_redirection_percentage as crp
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


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



week1['gameId'] = pd.to_numeric(week1['gameId'], errors='coerce')

# Step 1: Filter for Weeks 1-5 and 6-9
weeks_1_5 = week1[week1['gameId'] <= 2022101000]
weeks_6_9 = week1[week1['gameId'] > 2022101000]

weeks_1_5 = crp(weeks_1_5)
weeks_6_9 = crp(weeks_6_9)

# Step 2: Calculate Average Redirection% by Player
redirection_1_5 = weeks_1_5.groupby('nflId', as_index=False).agg({
    'redirection_percentage': 'mean',
    'total_plays': 'sum',  # Example: keep total plays
    'alignment_tag': 'first'  # Keep another column by first occurrence
})
redirection_6_9 = weeks_6_9.groupby('nflId', as_index=False).agg({
    'redirection_percentage': 'mean',
    'total_plays': 'sum',  # Example: keep total plays
    'alignment_tag': 'first'  # Keep another column by first occurrence
})
# Step 3: Merge Dataframes on Player ID
combined_data = pd.merge(redirection_1_5, redirection_6_9, on='nflId', suffixes=('_1_5', '_6_9'))


min_plays = 30  # Set the minimum number of plays
combined_data = combined_data[(combined_data['total_plays_1_5'] + 
                               combined_data['total_plays_6_9'])
                               >= min_plays]

# Step 4: Regression Analysis
X = combined_data[['redirection_percentage_1_5']]
y = combined_data['redirection_percentage_6_9']

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

# Step 5: Evaluate the Model
r2 = r2_score(y, y_pred)
print(f'R-squared: {r2:.4f}')

# Step 6: Plot Results
plt.figure(figsize=(8, 6))
plt.scatter(X, y, color='blue', label='Actual Data')
plt.plot(X, y_pred, color='red', label='Regression Line')
plt.xlabel('Redirection% (Weeks 1-5)')
plt.ylabel('Redirection% (Weeks 6-9)')
plt.title('Predictive Power of Redirection%')
plt.legend()
plt.show()

