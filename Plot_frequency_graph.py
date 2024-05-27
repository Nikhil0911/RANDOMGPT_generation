import numpy as np
import matplotlib.pyplot as plt

# Example data
data = np.array([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5])

# Sort the data
sorted_data = np.sort(data)

# Get unique values and their counts
unique_values, counts = np.unique(sorted_data, return_counts=True)

# Plot the frequency distribution
plt.bar(unique_values, counts, width=0.5, align='center', alpha=0.7, color='blue')

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Frequency Distribution')

# Show the plot
plt.show()
