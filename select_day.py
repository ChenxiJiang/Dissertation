#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 22:33:56 2017

@author: cicijiang
"""
import config
import pandas as pd

# load config
location = config.location
shopNo = config.shopNo
itemNo = config.itemNo
itemName = config.itemName

# read excel
df = pd.read_excel(location + 'Output_Xlsx/' + itemName + '_3hour.xlsx')

# set hour to 0
df['OptDate'] = df['OptDate'].apply(lambda x: x.replace(hour = 0))

# groupby day
df = df.groupby(['OptDate']).agg({'ItemCnt': 'sum'}).reset_index()

# clean dataframe
df.index = df['OptDate']
df = df.drop(['OptDate'], axis = 1)

# save data to file
df.to_csv(location + 'Output_Csv/' + itemName + '_day.csv')
df.to_excel(location + 'Output_Xlsx/' + itemName + '_day.xlsx')