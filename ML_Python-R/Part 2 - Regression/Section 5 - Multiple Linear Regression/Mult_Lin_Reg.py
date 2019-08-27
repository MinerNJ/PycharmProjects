from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dataset = pd.read_csv('50_Startups.csv')
x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 4].values

# The updated code for using OneHotEncoder.
ct = ColumnTransformer(
    [('one_hot_encoder', OneHotEncoder(), [3])],
    remainder='passthrough'
)
x = np.array(ct.fit_transform(x), dtype=np.float)

# Don't need to do this here, since the linear model removes one dummy variable
# automatically, but for other models one dummy variable will need to be dropped
# to prevent 'doubling' (1-D1=D2, 1-D2=D1, so having both D1 and D2 would be more
# than one, messes up the math.
# x = x[:, 1:]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

regressor = LinearRegression()
regressor.fit(x_train, y_train)

y_preds = regressor.predict(x_test)

# Backwards elimination for model selection
import statsmodels.regression.linear_model as sm

x = np.append(np.ones((50, 1)).astype(int), x, axis=1)
x_opt = x[:, [0, 1, 2, 3, 4, 5]]
regressor_OLS = sm.OLS(endog=y, exog=x_opt).fit()
regressor_OLS.summary()

# Model summary shows the x5 coefficient should be removed.
x_opt = x[:, [0, 1, 2, 3, 4]]
regressor_OLS = sm.OLS(y, x_opt).fit()
regressor_OLS.summary()
