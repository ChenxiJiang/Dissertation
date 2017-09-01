# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 21:11:49 2017

@author: cicijiang
"""
import config
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm  
from statsmodels.tsa.stattools import adfuller

# load config
location = config.location
itemName = config.itemName
seasonal = config.seasonal
interval = config.interval
plt.rcParams["figure.figsize"] = (10,5)

# load data
df = pd.read_csv(location + 'Output_Csv/' + itemName + '_' + seasonal + '.csv', header = 0)

def plot_graph(timeseries, tp):
    # plot data
    plt.figure(1)
    plt.plot(timeseries)
    plt.xlabel('Number of observations')
    plt.ylabel('Quantity')
    plt.savefig(location + 'Analyze/' + itemName + '_' + seasonal + '_line' + tp +'.png')
    plt.show()
    
    # plot histogram
    plt.figure(2)
    plt.subplot(211)
#    plt.xlabel('Quantity')
    plt.ylabel('Number of observations')
    timeseries.hist(bins=50)
    plt.subplot(212)
    plt.xlabel('Quantity')
    plt.ylabel('Density')
    timeseries.plot(kind='density')
    plt.savefig(location + 'Analyze/' + itemName + '_' + seasonal + '_density' + tp +'.png')
    plt.show()
    

def test_stationarity(timeseries, tp):
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    
    # write output into txt
    with open(location + 'Analyze/' + itemName + '_' + seasonal + '_ADF' + tp +'.txt', 'w') as f:
        f.write('Results of Dickey-Fuller Test:\n')
        for key,value in dfoutput.items():
            f.write('%s: %.3f\n' % (key, value))

print("\nOriginal")    
plot_graph(df['ItemCnt'], '')
test_stationarity(df['ItemCnt'], '')

#print("\nFirst Difference")  
#df['first_difference'] = df.ItemCnt - df.ItemCnt.shift(1)  
#test_stationarity(df.first_difference.dropna(inplace=False))

print("\nSeasonal Difference")  
df['seasonal_difference'] = df.ItemCnt - df.ItemCnt.shift(interval)  
plot_graph(df['seasonal_difference'].dropna(inplace=False), '_seasonal')
test_stationarity(df.seasonal_difference.dropna(inplace=False), '_seasonal')

#print("\nSeasonal First Difference")  
#df['seasonal_first_difference'] = df.first_difference - df.first_difference.shift(interval)  
#test_stationarity(df.seasonal_first_difference.dropna(inplace=False))

#fig = plt.figure(figsize=(12,8))
#ax1 = fig.add_subplot(211)
#fig = sm.graphics.tsa.plot_acf(df['ItemCnt'].iloc[0:], lags=40, ax=ax1)
#ax2 = fig.add_subplot(212)
#fig = sm.graphics.tsa.plot_pacf(df['ItemCnt'].iloc[0:], lags=40, ax=ax2)
#plt.savefig(location + 'Analyze/' + itemName + '_' + seasonal + '_ACF_PACF1.png')

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(df['seasonal_difference'].iloc[interval:], lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(df['seasonal_difference'].iloc[interval:], lags=40, ax=ax2)
plt.savefig(location + 'Analyze/' + itemName + '_' + seasonal + '_ACF_PACF.png')