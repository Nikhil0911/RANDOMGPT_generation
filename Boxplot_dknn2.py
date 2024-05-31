import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import NearestNeighbors

# Generate a sample dataset
np.random.seed(42)
data = np.random.normal(0, 1, 100)
data = np.append(data, [10, 15, -10])
df = pd.DataFrame(data, columns=['Values'])

# d-k-NN function
def calculate_knn_distances(data, k=5):
    nbrs = NearestNeighbors(n_neighbors=k+1).fit(data)
    distances, indices = nbrs.kneighbors(data)
    return distances[:, 1:]

# Adjusted boxplot function
def adjusted_boxplot(df, k=5):
    distances = calculate_knn_distances(df[['Values']], k)
    df['k_distances'] = np.mean(distances, axis=1)
    
    Q1 = df['Values'].quantile(0.25)
    Q3 = df['Values'].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    adj_lower_bound = df.loc[df['k_distances'] <= lower_bound, 'Values'].min()
    adj_upper_bound = df.loc[df['k_distances'] <= upper_bound, 'Values'].max()
    
    return adj_lower_bound, adj_upper_bound

# Plot function
def plot_adjusted_boxplot(df, adj_lower, adj_upper):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    # Original Boxplot
    ax[0].boxplot(df['Values'])
    ax[0].set_title('Original Boxplot')
    
    # Adjusted Boxplot
    df_adj = df[(df['Values'] >= adj_lower) & (df['Values'] <= adj_upper)]
    ax[1].boxplot(df_adj['Values'])
    ax[1].set_title('Adjusted Boxplot')
    
    plt.show()

# Calculate adjusted bounds
adj_lower, adj_upper = adjusted_boxplot(df, k=5)
# Plot adjusted boxplot
plot_adjusted_boxplot(df, adj_lower, adj_upper)
