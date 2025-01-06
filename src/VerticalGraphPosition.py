import pandas as pd
import matplotlib.pyplot as plt

normalized_data = pd.read_csv('Data/normalized_weeks.csv')

plt.figure(figsize=(10, 6))
plt.hist(normalized_data['x'], bins=200, color='skyblue', edgecolor='black')
plt.title('Distribution of Vertical Distance from the Ball')
plt.xlabel('Vertical distance')
plt.ylabel('Frequency')
plt.xlim(0, 7)
plt.grid(axis='y', alpha=0.75)
plt.show()
