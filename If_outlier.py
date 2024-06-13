import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

def isolation_forest_outliers(data, contamination):
    """
    Apply Isolation Forest to detect outliers with a given contamination level.

    Parameters:
    data (array-like): The dataset
    contamination (float): The proportion of outliers in the data

    Returns:
    array: Array indicating if a point is an outlier (-1) or not (1)
    """
    model = IsolationForest(contamination=contamination, random_state=42)
    model.fit(data)
    return model.predict(data)

# Generate example data
data = np.array([[1], [2], [2], [3], [3], [3], [4], [4], [4], [4], [5], [5], [6], [7], [8], [9], [10], [50], [60], [70]])

# Define a range of contamination values
contamination_values = np.linspace(0.01, 0.3, 30)

num_outliers = []

for contamination in contamination_values:
    outliers = isolation_forest_outliers(data, contamination)
    num_outliers.append(np.sum(outliers == -1))

# Plot the number of outliers vs. contamination
plt.figure(figsize=(10, 6))
plt.plot(contamination_values, num_outliers, marker='o', linestyle='-', color='b')
plt.title('Number of Outliers vs. Contamination')
plt.xlabel('Contamination')
plt.ylabel('Number of Outliers')
plt.grid(True)
plt.show()

# Determine best contamination
best_contamination = contamination_values[np.argmax(num_outliers)]
print(f"Best contamination parameter: {best_contamination}")

# Use the best contamination to detect outliers
outliers = isolation_forest_outliers(data, best_contamination)
print(f"Outliers: {data[outliers == -1]}")
