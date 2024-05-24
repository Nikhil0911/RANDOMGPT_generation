import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score, mean_squared_error
import statsmodels.api as sm

# Generate some example data (replace this with your actual data)
np.random.seed(42)
x = np.linspace(1, 100, 100)
y_linear = 2 * x + np.random.normal(0, 10, size=x.size)
y_quadratic = x ** 2 + np.random.normal(0, 100, size=x.size)
y_exponential = np.exp(0.05 * x) + np.random.normal(0, 5, size=x.size)

# Function to fit and evaluate models
def fit_and_evaluate(x, y):
    # Reshape x for sklearn
    x_reshaped = x.reshape(-1, 1)
    
    # Linear Model
    linear_model = LinearRegression()
    linear_model.fit(x_reshaped, y)
    y_pred_linear = linear_model.predict(x_reshaped)
    r2_linear = r2_score(y, y_pred_linear)
    mse_linear = mean_squared_error(y, y_pred_linear)
    
    # Quadratic Model
    poly_features = PolynomialFeatures(degree=2)
    x_poly = poly_features.fit_transform(x_reshaped)
    quadratic_model = LinearRegression()
    quadratic_model.fit(x_poly, y)
    y_pred_quadratic = quadratic_model.predict(x_poly)
    r2_quadratic = r2_score(y, y_pred_quadratic)
    mse_quadratic = mean_squared_error(y, y_pred_quadratic)
    
    # Exponential Model
    def exponential_func(x, a, b):
        return a * np.exp(b * x)
    
    popt, _ = curve_fit(exponential_func, x, y, maxfev=10000)
    y_pred_exponential = exponential_func(x, *popt)
    r2_exponential = r2_score(y, y_pred_exponential)
    mse_exponential = mean_squared_error(y, y_pred_exponential)
    
    # Plotting
    plt.figure(figsize=(14, 10))
    
    plt.subplot(3, 1, 1)
    plt.scatter(x, y, label='Data')
    plt.plot(x, y_pred_linear, color='red', label=f'Linear Fit (R² = {r2_linear:.2f}, MSE = {mse_linear:.2f})')
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.scatter(x, y, label='Data')
    plt.plot(x, y_pred_quadratic, color='green', label=f'Quadratic Fit (R² = {r2_quadratic:.2f}, MSE = {mse_quadratic:.2f})')
    plt.legend()
    
    plt.subplot(3, 1, 3)
    plt.scatter(x, y, label='Data')
    plt.plot(x, y_pred_exponential, color='purple', label=f'Exponential Fit (R² = {r2_exponential:.2f}, MSE = {mse_exponential:.2f})')
    plt.legend()
    
    plt.tight_layout()
    plt.show()
    
    return r2_linear, r2_quadratic, r2_exponential, mse_linear, mse_quadratic, mse_exponential

# Example usage
print("Linear Data:")
fit_and_evaluate(x, y_linear)

print("Quadratic Data:")
fit_and_evaluate(x, y_quadratic)

print("Exponential Data:")
fit_and_evaluate(x, y_exponential)
