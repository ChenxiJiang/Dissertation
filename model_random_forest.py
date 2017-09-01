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
from sklearn.ensemble import RandomForestRegressor
from sklearn.grid_search import GridSearchCV

# load config
location = config.location
itemName = config.itemName
seasonal = config.seasonal
plt.rcParams["figure.figsize"] = (20,5)

# set lag value
lag = config.interval

# read csv
df = pd.read_csv(location + 'Output_Csv/' + itemName + '_' + seasonal + '_train.csv', header = 0, index_col = 0)
df.index = df.index.to_datetime()

# split data into training set and validating set
train_size = int(len(df) * 0.8)
train, test = df[0:train_size], df[train_size:]

# creating lag features with pandas
#df['t+1'] = df.ItemCnt - df.ItemCnt.shift(interval)
df['t+1'] = df.ItemCnt
df = df.drop(['ItemCnt'], axis = 1)
for i in range(0, lag):
    df['t-' + str(i)] = df['t+1'].shift(i+1)
df = df.rename(columns = {'t-0': 't'})

# add weather feature
#df['Date'] = df.index
#df = df.set_index(df.index.date)
#df_weather = pd.read_excel(location + 'Output_Xlsx/weather.xlsx', header = 0)
#df_weather['Date'] = df_weather['Date'].apply(lambda x: x.date())
#df_weather = df_weather.set_index(df_weather['Date'])
#df_weather = df_weather.drop(['Date'], axis = 1)
#df = df.join(df_weather)
#df = df.set_index(df['Date'])
#df = df.drop(['Date'], axis = 1)

# drop nan rows
df = df.dropna()

# split differenced dataframe to XX and yy
X = df.drop(['t+1'], axis = 1)
y = df['t+1']

# split data into training set and validating set
train_size = train_size - lag
X_train, X_test = X[0:train_size], X[train_size:]
y_train, y_test = y[0:train_size], y[train_size:]

# Create random forest regression model
rfr = RandomForestRegressor()

# use grid search to find best parameter
SCORING = "neg_mean_squared_error"
FOLDS = 10 
parameters = {"n_estimators": [20, 60, 100], 
              "max_depth": [2, 6, 10, None],
              "max_features": ["auto", "sqrt", "log2", None]}
grid_search = GridSearchCV(estimator = rfr, param_grid = parameters, scoring = SCORING, cv = FOLDS)

# run random forest regression
result = grid_search.fit(X_train, y_train)

# summarize grid search result
def summarize(result):
    print("Best score of %f with %s" % (result.best_score_, result.best_params_))
    means, stdevs = [], []
    for params, mean_score, scores in result.grid_scores_:
        stdev = scores.std()
        means.append(mean_score)
        stdevs.append(stdev)
        print("Score of %f (stdev %f) with %r" % (mean_score, stdev, params))

summarize(result)

# fit model
rfr.set_params(**result.best_params_)
rfr.fit(X_train, y_train)

# predict testing data set
history = [x for x in train['ItemCnt'].values]
predictions = list()
for i in range(len(X_test)):
    yhat = rfr.predict(X_test.values[i,:].reshape(1, -1))[0]
    if (yhat < 0):
        yhat = 0
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

df_predictions.to_csv(location + 'Predictions/RandomForest/' + itemName + '_' + seasonal + '_predictions.csv')
df_predictions.to_excel(location + 'Predictions/RandomForest/' + itemName + '_' + seasonal + '_predictions.xlsx')

# errors
residuals = [test['ItemCnt'][i]-predictions[i] for i in range(len(test))]
df_residuals = pd.DataFrame(np.array(residuals).reshape(len(residuals), 1), columns = ['ItemCnt'])
print(df_residuals.describe())

# write output into txt
with open(location + 'Predictions/RandomForest/' + itemName + '_' + seasonal + '_matrix.txt', 'w') as f:
    f.write('Best Parameters: %s\n' % result.best_params_)
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
plt.savefig(location + 'Predictions/RandomForest/' + itemName + '_' + seasonal + '_1.png')
plt.show()

plt.figure(1)
styles = ['r-','b-']
df_predictions.plot(style=styles)
plt.savefig(location + 'Predictions/RandomForest/' + itemName + '_' + seasonal + '_2.png')
plt.show()

print(result.best_params_)