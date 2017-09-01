# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 14:15:48 2017

@author: cicijiang
"""

import config
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from math import sqrt 

# load config
location = config.location
names = ['toast', 'bread', 'sandwich', 'cube', 'snow', 'bean']

for name in names:
    globals()['df_%s_avg' % name] = pd.read_csv(location + 'Testing/' +name + '_3hour_predictions.csv', header = 0, index_col = 0)
    globals()['df_%s_avg' % name] = globals()['df_%s_avg' % name].drop(['Truth'], axis = 1)
    globals()['df_%s_avg' % name] = globals()['df_%s_avg' % name][2:]
    avg = globals()['df_%s_avg' % name].mean().values[0]
    globals()['df_%s_avg' % name]['Predict'] = globals()['df_%s_avg' % name]['Predict'].astype(int)
    
    tmp = []
    for i in range(545):
        tmp.append(avg*(i%5+1))
    tmp = pd.Series(tmp)
    tmp.index = globals()['df_%s_avg' % name].index
    globals()['df_%s_avg' % name]['Accumulated Q'] = tmp
    
    globals()['df_%s_avg' % name]['Accumulated Predict'] = 0
    for i in range(545):
        count = globals()['df_%s_avg' % name]['Predict'].ix[i]
        for j in range(i % 5):
            count += globals()['df_%s_avg' % name]['Predict'].ix[i-j-1]
        globals()['df_%s_avg' % name]['Accumulated Predict'].ix[i] = count
        
    globals()['df_%s_avg' % name]['Accumulated Q'] = globals()['df_%s_avg' % name]['Accumulated Q'].astype(int)    
    globals()['df_%s_avg' % name]['Difference'] = globals()['df_%s_avg' % name]['Accumulated Q'][4::5] - globals()['df_%s_avg' % name]['Accumulated Predict'][4::5]
    
    print(globals()['df_%s_avg' % name][4::5]['Difference'].mean())
    print(globals()['df_%s_avg' % name][4::5]['Difference'].std())
    
    globals()['df_%s' % name].to_excel(location + 'Operation/Production/' + name + '_average_production.xlsx')