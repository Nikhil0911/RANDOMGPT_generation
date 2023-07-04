import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.datasets import make_blobs

# Generate sample multidimensional data
X, _ = make_blobs(n_samples=100, centers=1, random_state=42)

# Function to calculate the distance to k nearest neighbors
def calculate_distance_to_k_nearest_neighbors(X, k=5):
    dist_matrix = cdist(X, X)  # Calculate pairwise distances
    k_nearest_neighbors = np.partition(dist_matrix, k, axis=1)[:, k]
    return k_nearest_neighbors

# Function to identify outliers using box plot adjustments
def identify_outliers_using_dknn(X, k=5, threshold=1.5):
    k_nearest_neighbors = calculate_distance_to_k_nearest_neighbors(X, k)
    num_dimensions = X.shape[1]

    outliers = []
    for dim in range(num_dimensions):
        q1, q3 = np.percentile(k_nearest_neighbors[:, dim], [25, 75])
        iqr = q3 - q1
        lower_bound = q1 - threshold * iqr
        upper_bound = q3 + threshold * iqr

        dim_outliers = np.where((k_nearest_neighbors[:, dim] < lower_bound) | (k_nearest_neighbors[:, dim] > upper_bound))
        outliers.extend(dim_outliers[0])

    outliers = list(set(outliers))  # Remove duplicate outliers

    return outliers

# Identify outliers using D-K-NN with box plot adjustments
outliers = identify_outliers_using_dknn(X, k=5, threshold=1.5)

# Plot the data points and highlight the outliers
plt.scatter(X[:, 0], X[:, 1], label='Data Points')
plt.scatter(X[outliers, 0], X[outliers, 1], color='red', label='Outliers')
plt.legend()
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.title('Outliers Identified using D-K-NN with Box Plot Adjustments')
plt.show()
