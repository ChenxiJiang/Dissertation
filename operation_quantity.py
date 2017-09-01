# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 22:06:10 2017

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
#name = config.itemName

for name in names:
    globals()['df_%s' % name] = pd.read_csv(location + 'Testing/' +name + '_3hour_predictions.csv', header = 0, index_col = 0)
    globals()['df_%s' % name] = globals()['df_%s' % name].drop(['Truth'], axis = 1)
    globals()['df_%s' % name]['Predict'] = globals()['df_%s' % name]['Predict'].astype(int)
    globals()['df_%s' % name] = globals()['df_%s' % name][2:]
    
    
    globals()['df_%s_production' % name] = pd.read_excel(location + 'Operation/Production/' +name + '_production.xlsx', header = 0, index_col = 0)
    lst = globals()['df_%s_production' % name]['Accumulated Q']
    tmp = []
    for i in range(545):
        tmp.append(lst.ix[i%5])
    tmp = pd.Series(tmp)
    tmp.index = globals()['df_%s' % name].index
    globals()['df_%s' % name]['Accumulated Q'] = tmp
    globals()['df_%s' % name]['Accumulated Predict'] = 0
    for i in range(545):
        count = globals()['df_%s' % name]['Predict'].ix[i]
        for j in range(i % 5):
            count += globals()['df_%s' % name]['Predict'].ix[i-j-1]
        globals()['df_%s' % name]['Accumulated Predict'].ix[i] = count
        
    globals()['df_%s' % name]['Accumulated Q'] = globals()['df_%s' % name]['Accumulated Q'].astype(int)
    globals()['df_%s' % name]['Difference'] = globals()['df_%s' % name]['Accumulated Q'][4::5] - globals()['df_%s' % name]['Accumulated Predict'][4::5]
    
    print(globals()['df_%s' % name][4::5]['Difference'].mean())
    print(globals()['df_%s' % name][4::5]['Difference'].std())
    
    globals()['df_%s' % name].to_excel(location + 'Operation/Production/' + name + '_predict_production.xlsx')