import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import skew
from statsmodels.stats.stattools import medcouple

def adjusted_boxplot(data, ax, model_name):
    # Calculate the medcouple statistic
    mc = medcouple(data)
    
    # Calculate the quartiles and IQR
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    
    # Adjust the whiskers based on the medcouple statistic
    if mc > 0:
        lower_whisker = q1 - 1.5 * np.exp(-4 * mc) * iqr
        upper_whisker = q3 + 1.5 * np.exp(3 * mc) * iqr
    else:
        lower_whisker = q1 - 1.5 * np.exp(-3 * mc) * iqr
        upper_whisker = q3 + 1.5 * np.exp(4 * mc) * iqr
    
    # Plot the boxplot
    ax.boxplot(data, whis=[lower_whisker, upper_whisker], vert=False, patch_artist=True)
    ax.set_title(f'{model_name} Model\n(Medcouple: {mc:.2f})')
    
# Generate data for the three models
np.random.seed(42)
n = 100

# Linear Model
linear_data = np.random.normal(loc=0, scale=1, size=n)

# Quadratic Model
quadratic_data = np.random.normal(loc=0, scale=1, size=n) ** 2

# Exponential Model
exponential_data = np.random.exponential(scale=1, size=n)

# Create subplots
fig, axs = plt.subplots(3, 1, figsize=(10, 15))

# Plot adjusted boxplots for each model
adjusted_boxplot(linear_data, axs[0], 'Linear')
adjusted_boxplot(quadratic_data, axs[1], 'Quadratic')
adjusted_boxplot(exponential_data, axs[2], 'Exponential')

# Show the plots
plt.tight_layout()
plt.show()
