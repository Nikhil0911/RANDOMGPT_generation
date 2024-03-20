import numpy as np

# Sample data representing heights of students (in inches)
heights = np.array([65, 68, 70, 72, 62, 66, 69, 71, 67, 68])

# Calculate mean and standard deviation
mean_height = np.mean(heights)
std_dev = np.std(heights)

#%%
# Set threshold as two standard deviations above the mean
threshold = mean_height + 2 * std_dev

print("Mean Height:", mean_height)
print("Standard Deviation:", std_dev)
print("Threshold:", threshold)

# Sample data representing test scores of students
scores = np.array([85, 90, 75, 80, 95, 88, 72, 78, 83, 92])

# Set threshold at the 90th percentile
threshold = np.percentile(scores, 90)

print("Threshold (90th percentile):", threshold)

#%%

import matplotlib.pyplot as plt

# Sample data representing ages of individuals
ages = np.array([25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75])

# Plot histogram
plt.hist(ages, bins=5)
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Histogram of Ages')
plt.show()

#%%
# Sample data representing monthly sales
sales = np.array([20000, 25000, 18000, 22000, 27000, 30000, 32000, 15000, 21000, 28000, 24000])

# Create box plot
plt.boxplot(sales)
plt.xlabel('Sales')
plt.title('Box Plot of Monthly Sales')
plt.show()

# Calculate upper whisker (Q3 + 1.5*IQR)
q3 = np.percentile(sales, 75)
iqr = np.percentile(sales, 75) - np.percentile(sales, 25)
upper_whisker = q3 + 1.5 * iqr

print("Threshold (Upper Whisker):", upper_whisker)

#%%
# Sample data representing test scores of students
scores = np.array([85, 90, 75, 80, 95, 88, 72, 78, 83, 92])

# Calculate z-scores
z_scores = (scores - np.mean(scores)) / np.std(scores)

# Set threshold as z-score of 1.5
threshold_z = 1.5

# Identify data points above threshold
outliers = scores[z_scores > threshold_z]

print("Threshold (Z-Score):", threshold_z)
print("Outliers:", outliers)

#%%
from sklearn.linear_model import LinearRegression

# Sample data representing hours studied and exam scores
hours_studied = np.array([3, 4, 5, 6, 7, 8, 9])
exam_scores = np.array([60, 65, 70, 75, 80, 85, 90])

# Fit linear regression model
model = LinearRegression()
model.fit(hours_studied.reshape(-1, 1), exam_scores)

# Predict exam score for a new value of hours studied
new_hours = 7.5
predicted_score = model.predict([[new_hours]])

print("Predicted Exam Score for {} hours studied: {:.2f}".format(new_hours, predicted_score[0]))

#%%
from sklearn.metrics import roc_curve, auc

# Sample data representing true labels and predicted probabilities
true_labels = np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
predicted_probs = np.array([0.2, 0.6, 0.3, 0.7, 0.4, 0.8, 0.1, 0.9, 0.5, 0.7])

# Calculate ROC curve and AUC
fpr, tpr, thresholds = roc_curve(true_labels, predicted_probs)
roc_auc = auc(fpr, tpr)

# Plot ROC curve
plt.plot(fpr, tpr, color='blue', lw=2, label='ROC curve (AUC = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--', label='Random Guess')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()

# Select threshold that maximizes AUC
optimal_threshold_index = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_threshold_index]

print("Optimal Threshold (Maximizing AUC):", optimal_threshold)

#%%
from sklearn.cluster import KMeans

# Sample data representing spending behavior of customers
spending_data = np.array([[100, 50], [150, 60], [200, 70], [80, 40], [120, 55], [190, 65]])

# Perform K-means clustering
kmeans = KMeans(n_clusters=2)
kmeans.fit(spending_data)

# Get cluster centers
cluster_centers = kmeans.cluster_centers_

# Calculate threshold based on distance between cluster centers
threshold_cluster = np.linalg.norm(cluster_centers[0] - cluster_centers[1])

print("Threshold (Cluster Distance):", threshold_cluster)

#%%
# Sample data representing daily stock prices
stock_prices = np.array([100, 105, 110, 115, 120, 115, 110, 105, 100, 95, 90])

# Calculate moving average
window_size = 3
moving_average = np.convolve(stock_prices, np.ones(window_size)/window_size, mode='valid')

# Calculate deviation from moving average
deviation = stock_prices[window_size-1:] - moving_average

# Set threshold as mean plus two standard deviations of deviation
threshold_time_series = np.mean(deviation) + 2 * np.std(deviation)

print("Threshold (Time Series Analysis):", threshold_time_series)

#%%
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve

# Sample data representing customer transactions and labels
X = np.array([[100, 0], [200, 1], [150, 0], [180, 1], [120, 0]])
y = np.array([0, 1, 0, 1, 0])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Random Forest classifier
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Predict probabilities for test data
y_probs = clf.predict_proba(X_test)[:, 1]

# Calculate precision-recall curve
precision, recall, thresholds = precision_recall_curve(y_test, y_probs)

# Select threshold that maximizes F1-score (harmonic mean of precision and recall)
f1_scores = 2 * (precision * recall) / (precision + recall)
optimal_threshold_index = np.argmax(f1_scores)
optimal_threshold_ml = thresholds[optimal_threshold_index]

print("Optimal Threshold (Maximizing F1-score):", optimal_threshold_ml)
