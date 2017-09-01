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
names = ['toast']

df_material = pd.read_excel(location + 'Operation/Material_Info.xlsx', header = 0, index_col = 0)
df_material.index = df_material['Product']
df_material = df_material.drop(['Product'], axis = 1)

df = pd.DataFrame()
for name in names:
    # load data
    globals()['df_%s' % name] = pd.read_csv(location + 'Testing/' +name + '_3hour_predictions.csv', header = 0, index_col = 0)
    globals()['df_%s' % name] = globals()['df_%s' % name][2:]
    # convert float to int
    globals()['df_%s' % name]['Predict'] = globals()['df_%s' % name]['Predict'].astype(int)
    if (name == 'sandwich'):
        material = pd.DataFrame(df_material.ix[name])
    else:
        material = pd.DataFrame(df_material.ix[name]).transpose()
    for i in range(len(material)):
        globals()['df_%s' % name]['%s_%s' % (name, material.ix[i][0])] = material.ix[i][1] * globals()['df_%s' % name]['Predict']
    

#    globals()['df_%s' % name]['%s_%s' % (name, df_material.ix[name]['Material'])] = df_material.ix[name]['Material'] * globals()['df_%s' % name]['Predict'] 
    globals()['avg_%s' % name] = globals()['df_%s' % name].mean()
    for index, value in globals()['avg_%s' % name][2:].iteritems():
        globals()['STD_%s' % index] = sqrt(globals()['df_%s' % name][index].std() * (5))
        globals()['TIL_%s' % index] = round(value*(5) + 2.05 * sqrt(globals()['df_%s' % name][index].std() * (5)))
#    df = df.append(globals()['df_%s' % name])
        inventory = [globals()['TIL_%s' % index]]
        item = globals()['df_%s' % name][index].tolist()
        order = []
        lack = []
        for i in range(1, len(item)+1):
            val = inventory[len(inventory) - 1] - item[i-1]
            if(val < 0):
                lack.append(-val)
                val = 0
            else:
                lack.append(0)
            inventory.append(val)
            if(i % 5 == 0):
                order.append(globals()['TIL_%s' % index] - inventory[len(inventory) - 1])
                inventory.append(globals()['TIL_%s' % index])
        
        base = datetime.datetime(2017,7,1,8,0,0)
        full_list = [base - datetime.timedelta(hours=x) for x in range(0, 24 * 109 + 1)]
        full_list = [x for x in full_list if x.hour in [8,11,14,17,20,23]]
        full_list = full_list[::-1]
        
        sub_list = [x for x in full_list if x.hour in [8,11,14,17,20]]
        order_list = sub_list[0::5][1:]
        lack_list = sub_list[:-1]
        
        inventory = pd.DataFrame(inventory)
        inventory.index = full_list
        inventory.columns = ['Inventory']
        
        order = pd.DataFrame(order)
        order.index = order_list
        order.columns = ['Order']
        
        lack = pd.DataFrame(lack)
        lack.index = lack_list
        lack.columns = ['Lack']
        
        inventory = inventory.join(globals()['df_%s' % name][index])
        inventory = inventory.join(order)
        inventory = inventory.join(lack)
    
        inventory.rename(columns = {index: 'Sold'}, inplace = True)
        inventory.to_csv(location + 'Operation/Inventory/' + index + '_inventory.csv')
#    plt.figure(1)
#    inventory[0:12].plot()
#    plt.axhline(y=globals()['TIL_%s' % name], linestyle = '--', color = 'g')
#    plt.show()