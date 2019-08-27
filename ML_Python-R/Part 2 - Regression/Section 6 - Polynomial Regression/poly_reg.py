import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

dataset = pd.read_csv('Position_Salaries.csv')
x = dataset.iloc[:, 1:2].values
y = dataset.iloc[:, 2].values

# Basic linear regression model for comparison
lin_reg = LinearRegression()
lin_reg.fit(x, y)

# Transforming matrix x into a polynomial matrix
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree=2)
x_poly = poly_reg.fit_transform(x)

# Creating a new linear regression model built off of polynomial feature matrix x
lin_reg_2 = LinearRegression()
lin_reg_2.fit(x_poly, y)

# Visualizing linear regression results
plt.scatter(x, y, color='red')
plt.plot(x, lin_reg.predict(x), color='blue')
plt.title('Linear Regression Results')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()

# Visualizing polynomial regression results
plt.scatter(x, y, color='red')
# Not using the x_poly because it was already fit to x when x was a different feature matrix.
plt.plot(x, lin_reg_2.predict(poly_reg.fit_transform(x)), color='blue')
plt.title('Polynomial Regression Results')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()

# Changing the degree to 3 to better fit the model to data
poly_reg = PolynomialFeatures(degree=3)
x_poly = poly_reg.fit_transform(x)

lin_reg_2 = LinearRegression()
lin_reg_2.fit(x_poly, y)

# Visualizing polynomial regression results
plt.scatter(x, y, color='red')
# Not using the x_poly because it was already fit to x when x was a different feature matrix.
plt.plot(x, lin_reg_2.predict(poly_reg.fit_transform(x)), color='blue')
plt.title('Polynomial Regression Results')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()

# Adding another degree... and the model nails the data.
poly_reg = PolynomialFeatures(degree=4)
x_poly = poly_reg.fit_transform(x)

lin_reg_2 = LinearRegression()
lin_reg_2.fit(x_poly, y)

# Visualizing polynomial regression results
plt.scatter(x, y, color='red')
plt.plot(x, lin_reg_2.predict(poly_reg.fit_transform(x)), color='blue')
plt.title('Polynomial Regression Results')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()

# Improving the model by reducing the "step size" from 1 unit to .1 -- smoothing the curve of the model
x_grid = np.arange(min(x), max(x), 0.1)
# Reshaping x_grid into a matrix where the number of rows is the same as x_grid with 1 column
x_grid = x_grid.reshape((len(x_grid), 1))
plt.scatter(x, y, color='red')
plt.plot(x_grid, lin_reg_2.predict(poly_reg.fit_transform(x_grid)), color='blue')
plt.title('Polynomial Regression Results')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()

# predicting a salary corresponding to the level of 6.5 with the linear model - $330k
lin_reg.predict([[6.5]])

# predicting a salary corresponding to the level of 6.5 with the linear model - $150k
lin_reg_2.predict(poly_reg.fit_transform([[6.5]]))
