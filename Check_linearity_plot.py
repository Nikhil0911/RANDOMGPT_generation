import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Sample data (you can replace this with your own data)
x_data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
y_data = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256, 512])

# Define model functions
def linear_model(x, a, b):
    return a * x + b

def quadratic_model(x, a, b, c):
    return a * x**2 + b * x + c

def exponential_model(x, a, b, c):
    return a * np.exp(b * x) + c

# Fit models to data
params_linear, _ = curve_fit(linear_model, x_data, y_data)
params_quadratic, _ = curve_fit(quadratic_model, x_data, y_data)
params_exponential, _ = curve_fit(exponential_model, x_data, y_data, maxfev=10000)

# Generate fitted data
x_fit = np.linspace(min(x_data), max(x_data), 100)
y_fit_linear = linear_model(x_fit, *params_linear)
y_fit_quadratic = quadratic_model(x_fit, *params_quadratic)
y_fit_exponential = exponential_model(x_fit, *params_exponential)

# Plot data and fitted models
plt.figure(figsize=(10, 6))
plt.scatter(x_data, y_data, label='Data', color='black')
plt.plot(x_fit, y_fit_linear, label='Linear fit', color='red')
plt.plot(x_fit, y_fit_quadratic, label='Quadratic fit', color='blue')
plt.plot(x_fit, y_fit_exponential, label='Exponential fit', color='green')
plt.legend()
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Data Fitting: Linear, Quadratic, and Exponential Models')
plt.show()
