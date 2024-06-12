import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

# Step 1: Load your data
df = pd.read_csv('your_data.csv')  # Replace with your data loading method
X = df[['data']].values  # Convert to 2D array as LOF requires 2D input

# Step 2: Calculate LOF scores
lof = LocalOutlierFactor(novelty=False)
lof.fit(X)
lof_scores = -lof.negative_outlier_factor_  # LOF scores (higher means more abnormal)

# Step 3: Define thresholds for varying numbers of outliers
def find_threshold(lof_scores, contamination):
    sorted_scores = np.sort(lof_scores)
    threshold_index = int((1 - contamination) * len(sorted_scores))
    return sorted_scores[threshold_index]

# Step 4: Perform grid search to find the best hyperparameters
param_grid = {
    'lof__n_neighbors': [5, 10, 15, 20],
    'lof__contamination': [0.01, 0.05, 0.1, 0.2]  # Dummy values for GridSearchCV compatibility
}

# Define a Pipeline with LOF
pipeline = Pipeline([
    ('lof', LocalOutlierFactor(novelty=False))
])

# GridSearchCV for LOF
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy', n_jobs=-1)

# As LOF is unsupervised, we need to create pseudo labels: 1 for normal, -1 for outliers based on variable contamination
best_params = None
best_score = -np.inf

for contamination in param_grid['lof__contamination']:
    threshold = find_threshold(lof_scores, contamination)
    y_pseudo = np.where(lof_scores > threshold, -1, 1)

    # Fit grid search with pseudo labels
    grid_search.fit(X, y_pseudo)
    
    if grid_search.best_score_ > best_score:
        best_score = grid_search.best_score_
        best_params = grid_search.best_params_

print(f"Best parameters: {best_params}")
print(f"Best score: {best_score}")

# Use the best parameters to initialize and fit the LOF model
best_lof = LocalOutlierFactor(n_neighbors=best_params['lof__n_neighbors'], novelty=False)
best_lof.fit(X)
best_lof_scores = -best_lof.negative_outlier_factor_

# Set the threshold based on the best contamination found
best_threshold = find_threshold(best_lof_scores, best_params['lof__contamination'])

# Predictions using the best threshold
predictions = np.where(best_lof_scores > best_threshold, -1, 1)
print(f"Predictions: {predictions}")
