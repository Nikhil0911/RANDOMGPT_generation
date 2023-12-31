import numpy as np
from scipy.spatial.distance import cdist
from sklearn.datasets import make_blobs

# Generate sample multidimensional data
X, _ = make_blobs(n_samples=100, centers=1, random_state=42)

# Function to calculate the distance to k nearest neighbors
def calculate_distance_to_k_nearest_neighbors(X, k=5):
    dist_matrix = cdist(X, X)  # Calculate pairwise distances
    k_nearest_neighbors = np.partition(dist_matrix, k, axis=1)[:, k]
    return k_nearest_neighbors

# Function to estimate local densities using D-K-NN Scheme 3
def estimate_local_densities(X, k=5):
    k_nearest_neighbors = calculate_distance_to_k_nearest_neighbors(X, k)
    local_densities = 1 / (k_nearest_neighbors ** X.shape[1])
    return local_densities

# Function to calculate the joint probability density using D-K-NN Scheme 3
def calculate_joint_probability_density(X, k=5):
    local_densities = estimate_local_densities(X, k)
    joint_prob_density = local_densities / np.sum(local_densities)
    return joint_prob_density

# Calculate the joint probability density using D-K-NN Scheme 3
joint_prob_density = calculate_joint_probability_density(X, k=5)

# Create a contour plot to visualize the joint probability density
plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=joint_prob_density, cmap='viridis', edgecolors='k')
plt.colorbar(label='Joint Probability Density')
plt.xlabel('Dimension 1')
plt.ylabel('Dimension 2')
plt.title('Joint Probability Density Estimation using D-K-NN Scheme 3')
plt.show()
