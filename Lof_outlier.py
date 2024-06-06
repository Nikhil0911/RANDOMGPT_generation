import numpy as np
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
import matplotlib.pyplot as plt
import seaborn as sns

# Generate or load the dataset
np.random.seed(42)
data = np.random.exponential(scale=2, size=1000)  # Left-skewed data
data = np.append(data, [50, 60, 70])  # Add some outliers
df = pd.DataFrame(data, columns=['amount'])

# Visualize the data
sns.histplot(df['amount'], bins=50, kde=True)
plt.title('Histogram of Amounts')
plt.show()

# Apply log transformation to handle left skewness
df['log_amount'] = np.log1p(df['amount'])  # log1p is log(1 + x) to handle zero values
sns.histplot(df['log_amount'], bins=50, kde=True)
plt.title('Histogram of Log-Transformed Amounts')
plt.show()

# Fit the LOF model
lof = LocalOutlierFactor(n_neighbors=20, contamination=0.01)  # Adjust n_neighbors and contamination as needed
df['lof_score'] = lof.fit_predict(df[['log_amount']])
df['lof_score'] = -lof.negative_outlier_factor_

# Identify outliers
threshold = np.percentile(df['lof_score'], 95)  # Adjust percentile as needed
df['is_outlier'] = df['lof_score'] > threshold
outliers = df[df['is_outlier']]

# Visualize the results
plt.figure(figsize=(10, 6))
plt.scatter(df['log_amount'], df['lof_score'], c=df['is_outlier'], cmap='coolwarm')
plt.xlabel('Log Amount')
plt.ylabel('LOF Score')
plt.title('LOF Scores and Outliers')
plt.show()

# Print and analyze outliers
print("Outliers detected:")
print(outliers)
