import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def create_boxplot(data):
    """
    Function to create a box plot of the given data using Seaborn.

    Parameters:
        data (array-like): The data to plot.
    """
    plt.figure(figsize=(8, 6))
    sns.boxplot(data=data)
    plt.title("Box Plot of Data")
    plt.xlabel("Data")
    plt.ylabel("Values")
    plt.show()

def get_whisker(data, thold):
  q1 = np.percentile(data, 25)
  q3 = np.percentile(data, 75)
  iqr = q3-q1
  whisker = q3 + thold * iqr
  return whisker

def plot_lineplot(data, thresholds = [1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3]):
    """
    Function to plot a line plot of data points beyond upper whisker vs different thresholds using Seaborn.

    Parameters:
        data (array-like): The data to analyze.
        thresholds (array-like): The threshold values ranging between 1 to 5.
    """
    exceeding_data_counts = []

    for threshold in thresholds:
        whisker = get_whisker(data, threshold)
        exceeding_data_count = len(data[data > whisker])
        exceeding_data_counts.append(exceeding_data_count)

    plt.figure(figsize=(8, 6))
    sns.lineplot(x=thresholds, y=exceeding_data_counts, marker='o')
    plt.title("Line Plot of Data Points Beyond Upper Whisker vs Thresholds")
    plt.xlabel("Threshold")
    plt.ylabel("Number of Data Points Beyond Upper Whisker")
    plt.grid(True)
    plt.show()

def final_boxplot(data, final_threshold):
    """
    Function to draw a box plot with removing all other data beyond the finalized whisker using Seaborn.

    Parameters:
        data (array-like): The data to analyze.
        final_threshold (float): The finalized threshold value.
    """
    whisker = get_whisker(data, final_threshold)
    filtered_data = data[data <= whisker]

    plt.figure(figsize=(8, 6))
    sns.boxplot(data=filtered_data)
    plt.title(f"Final Box Plot (Whisker Threshold = {final_threshold})")
    plt.xlabel("Filtered Data")
    plt.ylabel("Values")
    plt.show()

# Sample data
np.random.seed(0)
data = np.random.normal(loc=0, scale=1, size=100)

# Create a box plot of the data
create_boxplot(data)

# Define thresholds ranging from 1 to 5 with a step of 0.25
thresholds = np.arange(1, 5.25, 0.25)

# Plot line plot of data points beyond upper whisker vs different thresholds
plot_lineplot(data, thresholds)

# Finalize a threshold value (for example, 2.5)
final_threshold = 2.5

# Draw final box plot with removing all other data beyond the finalized whisker
final_boxplot(data, final_threshold)
