## Data Preprocessing

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import Imputer, LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('Data.csv')

x = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 3].values

##Imputer recognizes missing values and then adds the values into the data.
imputer = Imputer
imputer = Imputer(missing_values = 'NaN', strategy = 'mean', axis = 0)
imputer = imputer.fit(x[:, 1:3])
x[:, 1:3] = imputer.transform(x[:, 1:3])

##Encoding the country names (col 0) 
labelencoder_x = LabelEncoder()
x[:,0] = labelencoder_x.fit_transform(x[:,0])

##Creating dummy variables for countries so the ML model recognizes them as
##categorical data and not ordered data.
onehotencoder = OneHotEncoder(categorical_features = [0])
x = onehotencoder.fit_transform(x).toarray()

##Encoding purchased column (col 3) from yes/no to 1/0, hotencoder not 
#required since there's only 2 categories.
labelencoder_y = LabelEncoder()
y = labelencoder_y.fit_transform(y)

##Splitting data into training and test sets, random_state is seed
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, 
                                                    random_state = 0)

##Feature scaling - scale the training data first, then the test
x_scale = StandardScaler()
x_train = x_scale.fit_transform(x_train)
x_test = x_scale.transform(x_test)