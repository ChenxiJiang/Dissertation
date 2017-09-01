#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 22:18:12 2017

@author: cicijiang
"""
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error 
from sklearn.metrics import mean_absolute_error 
from statsmodels.tsa.arima_model import ARIMA 

# load config
location = config.location
itemName = config.itemName
seasonal = config.seasonal
interval = config.interval
plt.rcParams["figure.figsize"] = (20,5)

# read csv
df = pd.read_csv(location + 'Output_Csv/' + itemName + '_' + seasonal + '_train.csv', header = 0, index_col = 0)
df.index = df.index.to_datetime()
df['ItemCnt'] = df['ItemCnt'].astype(float)

# split data into training set and validating set
train_size = int(len(df) * 0.8)
train, test = df[0:train_size], df[train_size:]

def difference(dataset, interval): 
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value) 
    return diff

def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]

# arima validation
history = [x for x in train['ItemCnt'].values]

#diff = difference(history, 5)
predictions = list()
for i in range(len(test)):
        # difference data
        diff = difference(history, interval)
        # predict
        model = ARIMA(diff, order=(2,0,2))
        model_fit = model.fit(trend='c', disp=False)
        yhat = model_fit.forecast()[0]
#        yhat = yhat[0]

        yhat = inverse_difference(history, yhat, interval)
        if (yhat < 0):
            yhat = 0    
        predictions.append(yhat)
        # observation
        obs = test['ItemCnt'][i]
        history.append(obs)
        print('>Predicted=%.3f, Expected=%.3f' % (yhat, obs))

rmse = sqrt(mean_squared_error(test, predictions)) 
print('RMSE: %.3f' % rmse)
mae = mean_absolute_error(test, predictions)
print('MAE: %.3f' % mae)

# save data to txt
predictions = [[0] if (x == 0) else x for x in predictions]
df_predictions = pd.DataFrame(predictions, index = test.index, columns = ['Predict'])
df_predictions['Truth'] = test['ItemCnt']

df_predictions.to_csv(location + 'Predictions/ARIMA/' + itemName + '_' + seasonal + '_predictions.csv')
df_predictions.to_excel(location + 'Predictions/ARIMA/' + itemName + '_' + seasonal + '_predictions.xlsx')

# errors
residuals = [test['ItemCnt'][i]-predictions[i] for i in range(len(test))]
df_residuals = pd.DataFrame(np.array(residuals).reshape(len(residuals), 1), columns = ['ItemCnt'])
print(df_residuals.describe())

# write output into txt
with open(location + 'Predictions/ARIMA/' + itemName + '_' + seasonal + '_matrix.txt', 'w') as f:
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
plt.savefig(location + 'Predictions/ARIMA/' + itemName + '_' + seasonal + '_1.png')
plt.show()

plt.figure(1)
styles = ['r-','b-']
df_predictions.plot(style=styles)
plt.savefig(location + 'Predictions/ARIMA/' + itemName + '_' + seasonal + '_2.png')
plt.show()