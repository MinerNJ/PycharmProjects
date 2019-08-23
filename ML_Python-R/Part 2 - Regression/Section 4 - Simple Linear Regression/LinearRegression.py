import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

dataset = pd.read_csv('Salary_Data.csv')
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:,1].values

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=(1/3), random_state=0)

##importing linear regression and fitting it to the training data
regressor = LinearRegression()
regressor.fit(x_train, y_train)

##predicting y(salary) values based off of the training data
y_preds = regressor.predict(x_test)

##plotting the training data as red points and the predicted y values as a 
##linear line in blue. 
plt.scatter(x_train, y_train, color='red')
plt.plot(x_train, regressor.predict(x_train), color='blue')
plt.title('Salary vs Experience (Training Set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()

##plotting test data with y(salary) values predicted from a linear model 
##trained on the test data and show in blue.
plt.scatter(x_test, y_test, color='red')
plt.plot(x_train, regressor.predict(x_train), color='blue')
plt.title('Salary vs Experience(Test Set)')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.show()
