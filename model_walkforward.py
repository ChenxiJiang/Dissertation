#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 19:51:38 2017

@author: cicijiang
"""
import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from sklearn.metrics import mean_squared_error 
from sklearn.metrics import mean_absolute_error 

# load config
location = config.location
itemName = config.itemName
seasonal = config.seasonal
plt.rcParams["figure.figsize"] = (20,5)

# read csv
df = pd.read_csv(location + 'Output_Csv/' + itemName + '_' + seasonal + '_train.csv', header = 0, index_col = 0)
df.index = df.index.to_datetime()

# split data into training set and validating set
train_size = int(len(df) * 0.8)
train, test = df[0:train_size], df[train_size:]

# walk-forward validation
history = [x for x in train['ItemCnt']] 
predictions = list()
for i in range(len(test)):
    # predict
    yhat = history[-1]
    predictions.append(yhat)
    # observation
    obs = test['ItemCnt'][i]
    history.append(obs)
    print('>Predicted=%.3f, Expected=%3.f' % (yhat, obs))
    
# evaluate results
rmse = sqrt(mean_squared_error(test, predictions)) 
print('RMSE: %.3f' % rmse)
mae = mean_absolute_error(test, predictions)
print('MAE: %.3f' % mae)

# save data to txt
df_predictions = pd.DataFrame(predictions, index = test.index, columns = ['Predict'])
df_predictions['Truth'] = test['ItemCnt']

df_predictions.to_csv(location + 'Predictions/Walkforward/' + itemName + '_' + seasonal + '_predictions.csv')
df_predictions.to_excel(location + 'Predictions/Walkforward/' + itemName + '_' + seasonal + '_predictions.xlsx')

# errors
residuals = [test['ItemCnt'][i]-predictions[i] for i in range(len(test))]
df_residuals = pd.DataFrame(np.array(residuals).reshape(len(residuals), 1), columns = ['ItemCnt'])
print(df_residuals.describe())

# write output into txt
with open(location + 'Predictions/Walkforward/' + itemName + '_' + seasonal + '_matrix.txt', 'w') as f:
    f.write('RMSE: %.3f\n' % rmse)
    f.write('MAE: %.3f\n' % mae)
    f.write('\nResiduals Describe:\n')
    for i in range(len(df_residuals.describe())):
        f.write('%s: %.3f\n' % (df_residuals.describe().index[i], df_residuals.describe().values[i]))
        
# plot prediction against test
df_predictions = df_predictions.reset_index() 
styles = ['r-','b-']

plt.figure(0)
df_predictions[0:50].plot(style=styles)
plt.savefig(location + 'Predictions/Walkforward/' + itemName + '_' + seasonal + '_1.png')
plt.show()

plt.figure(1)
df_predictions.plot(style=styles)
plt.savefig(location + 'Predictions/Walkforward/' + itemName + '_' + seasonal + '_2.png')
plt.show()