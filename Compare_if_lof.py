from sklearn.datasets import make_blobs
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import davies_bouldin_score, calinski_harabasz_score
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances

# Generate sample data
X, y = make_blobs(n_samples=1000, centers=4, random_state=42)

# Create clustering model (KMeans) for comparison
kmeans = KMeans(n_clusters=4, random_state=42)
kmeans_labels = kmeans.fit_predict(X)

# Isolation Forest
isolation_forest = IsolationForest(random_state=42)
isolation_forest.fit(X)
isolation_forest_labels = isolation_forest.predict(X)

# Local Outlier Factor
lof = LocalOutlierFactor(n_neighbors=20, novelty=True)
lof.fit(X)
lof_scores = -lof.decision_function(X)
lof_labels = lof.predict(X)

# Evaluation metrics
def davies_bouldin_index(X, labels):
    return davies_bouldin_score(X, labels)

def calinski_harabasz_index(X, labels):
    return calinski_harabasz_score(X, labels)

def dunn_index(X, labels):
    distances = euclidean_distances(X)
    min_intercluster_distances = []
    max_intracluster_distances = []

    for label in set(labels):
        cluster_points = X[labels == label]
        cluster_distances = distances[labels == label][:, labels == label]
        if len(cluster_points) > 1:
            min_intercluster_distances.append(cluster_distances.min())
        max_intracluster_distances.append(cluster_distances.max())

    min_intercluster_distance = min(min_intercluster_distances)
    max_intracluster_distance = max(max_intracluster_distances)
    dunn_index = min_intercluster_distance / max_intracluster_distance

    return dunn_index

# Compute metrics for KMeans
kmeans_db_index = davies_bouldin_index(X, kmeans_labels)
kmeans_ch_index = calinski_harabasz_index(X, kmeans_labels)
kmeans_dunn_index = dunn_index(X, kmeans_labels)

# Compute metrics for Isolation Forest
isolation_forest_db_index = davies_bouldin_index(X, isolation_forest_labels)
isolation_forest_ch_index = calinski_harabasz_index(X, isolation_forest_labels)
isolation_forest_dunn_index = dunn_index(X, isolation_forest_labels)

# Compute metrics for Local Outlier Factor
lof_db_index = davies_bouldin_index(X, lof_labels)
lof_ch_index = calinski_harabasz_index(X, lof_labels)
lof_dunn_index = dunn_index(X, lof_labels)

# Print metrics
print("KMeans:")
print(f"Davies-Bouldin Index: {kmeans_db_index}")
print(f"Calinski-Harabasz Index: {kmeans_ch_index}")
print(f"Dunn Index: {kmeans_dunn_index}")
print()
print("Isolation Forest:")
print(f"Davies-Bouldin Index: {isolation_forest_db_index}")
print(f"Calinski-Harabasz Index: {isolation_forest_ch_index}")
print(f"Dunn Index: {isolation_forest_dunn_index}")
print()
print("Local Outlier Factor:")
print(f"Davies-Bouldin Index: {lof_db_index}")
print(f"Calinski-Harabasz Index: {lof_ch_index}")
print(f"Dunn Index: {lof_dunn_index}")
