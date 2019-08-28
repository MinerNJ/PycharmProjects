import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.preprocessing import scale, StandardScaler

dataset = pd.read_csv('Position_Salaries.csv')
x = dataset.iloc[:, 1:2].values
y = dataset.iloc[:, 2].values

# SVR class does not automatically apply feature scaling like the other linear regression models do, so we must
# scale the features for an accurate model. Both feature matrix x and dependent variable vector y must be scaled.
sc_x = StandardScaler()
sc_y = StandardScaler()
x = sc_x.fit_transform(x)
# StandardScaler only works on features, not target data. Even though y has the same dimensions as x (an array),
# StandardScaler won't accept it. To get SS to take it, the dependent variable y must be reshaped with NumPy from
# an array (1D row) form into a vector (2D column) form. SS takes y as a vector, but the SVR is expecting y as a
# 1D array, so y must be flattened from a vector back into an array. So: y -> reshaped -> scaled -> reshaped.
y = np.array(y).reshape(-1, 1)
y = sc_y.fit_transform(y)
y = y.flatten()


# rbf is the default kernel for SVR
regressor = SVR(kernel='rbf')
regressor.fit(x, y)

y_preds = sc_y.inverse_transform(regressor.predict(sc_x.fit_transform(np.array([[6.5]]))))

plt.scatter(x, y, color='red')
plt.plot(x, regressor.predict(x), color='blue')
plt.title('Support Vector Regression')
plt.xlabel('Position Level')
plt.ylabel('Salary')
plt.show()
