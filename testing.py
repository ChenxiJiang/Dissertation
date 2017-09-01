# -*- coding: utf-8 -*-
"""
Created on Thu Aug 17 14:53:19 2017

@author: cicijiang
"""

import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error 
from sklearn.metrics import mean_absolute_error 
from sklearn.ensemble import RandomForestRegressor

# load config
location = config.location
itemName = config.itemName
seasonal = config.seasonal
plt.rcParams["figure.figsize"] = (20,5)

# set lag value
lag = config.interval

# read csv
df = pd.read_csv(location + 'Output_Csv/' + itemName + '_' + seasonal + '.csv', header = 0, index_col = 0)
df_train = pd.read_csv(location + 'Output_Csv/' + itemName + '_' + seasonal + '_train.csv', header = 0, index_col = 0)
df_test = pd.read_csv(location + 'Output_Csv/' + itemName + '_' + seasonal + '_test.csv', header = 0, index_col = 0)

df.index = df.index.to_datetime()
df_train.index = df_train.index.to_datetime()
df_test.index = df_test.index.to_datetime()

# creating lag features with pandas
#df['t+1'] = df.ItemCnt - df.ItemCnt.shift(interval)
df['t+1'] = df.ItemCnt
df = df.drop(['ItemCnt'], axis = 1)
for i in range(0, lag):
    df['t-' + str(i)] = df['t+1'].shift(i+1)
df = df.rename(columns = {'t-0': 't'})

# drop nan rows
df = df.dropna()

# split differenced dataframe to XX and yy
X = df.drop(['t+1'], axis = 1)
y = df['t+1']

# split data into training set and validating set
train_size = len(df_train) - lag
X_train, X_test = X[0:train_size], X[train_size:]
y_train, y_test = y[0:train_size], y[train_size:]

# Create random forest regression model
rfr = RandomForestRegressor(n_estimators = 100, max_depth = 6, max_features = 'sqrt')

# fit model
rfr.fit(X_train, y_train)

# predict testing data set
history = [x for x in df_train['ItemCnt'].values]
predictions = list()
for i in range(len(X_test)):
    yhat = rfr.predict(X_test.values[i,:].reshape(1, -1))[0]
    if (yhat < 0):
        yhat = 0
    predictions.append(yhat)
    # observation
    obs = df_test['ItemCnt'][i]
    history.append(obs)
    print('>Predicted=%.3f, Expected=%3.f' % (yhat, obs))

# evaluate results
rmse = sqrt(mean_squared_error(y_test, predictions)) 
print('RMSE: %.3f' % rmse)
mae = mean_absolute_error(y_test, predictions)
print('MAE: %.3f' % mae)

# save data to txt
df_predictions = pd.DataFrame(predictions, index = y_test.index, columns = ['Predict'])
df_predictions['Truth'] = df_test['ItemCnt']

df_predictions.to_csv(location + 'Testing/' + itemName + '_' + seasonal + '_predictions.csv')
df_predictions.to_excel(location + 'Testing/' + itemName + '_' + seasonal + '_predictions.xlsx')

# errors
residuals = [df_test['ItemCnt'][i]-predictions[i] for i in range(len(df_test))]
df_residuals = pd.DataFrame(np.array(residuals).reshape(len(residuals), 1), columns = ['ItemCnt'])
print(df_residuals.describe())

# write output into txt
with open(location + 'Testing/' + itemName + '_' + seasonal + '_matrix.txt', 'w') as f:
    f.write('RMSE: %.3f\n' % rmse)
    f.write('MAE: %.3f\n' % mae)
    f.write('\nResiduals Describe:\n')
    for i in range(len(df_residuals.describe())):
        f.write('%s: %.3f\n' % (df_residuals.describe().index[i], df_residuals.describe().values[i]))

# plot prediction against test
df_predictions = df_predictions.reset_index() 
plt.figure(0)
styles = ['r-','b-']
df_predictions[0:50].plot(style=styles)
plt.savefig(location + 'Testing/' + itemName + '_' + seasonal + '_1.png')
plt.show()

plt.figure(1)
styles = ['r-','b-']
df_predictions.plot(style=styles)
plt.savefig(location + 'Testing/' + itemName + '_' + seasonal + '_2.png')
plt.show()
