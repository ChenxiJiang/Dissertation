# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 20:22:31 2017

@author: cicijiang
"""

location = '/Users/cicijiang/Desktop/Dissertation/'

dict_itemName_itemNo = {'toast':10401144, 'bread': 10401123, 'cube': 10401069, 'sandwich': 10403012, 'snow': 10401041, 'bean': 10401091}
dict_seasonal_interval = {'3hour': 5, 'day': 7}

shopNo = 2102

itemName = 'toast'
#itemName = 'bread'
#itemName = 'cube'
#itemName = 'sandwich'
#itemName = 'snow'
#itemName = 'bean'

itemNo = dict_itemName_itemNo[itemName]

seasonal = '3hour'
#seasonal = 'day'
interval = dict_seasonal_interval[seasonal]
