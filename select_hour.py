#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 23:39:28 2017

@author: cicijiang
"""
import config
import pandas as pd
import numpy as np
import datetime
import math
import scipy.stats

# load config
location = config.location
shopNo = config.shopNo
itemNo = config.itemNo
itemName = config.itemName

# read excel
df = pd.read_excel(location + 'Output_Xlsx/items_hour_' + str(shopNo) + '.xlsx')

# select toast by 'ItemNo'
df_item = df[(df['ItemNo'] == itemNo)]

# set 'ItemCnt' to 0 if it is less than 0
df_item['ItemCnt'] = df_item['ItemCnt'].apply(lambda x: 0 if x < 0 else x)

# add feature hour
df_item['hour'] = [x.hour for x in df_item['OptDate']]

# find all missing date
base = datetime.datetime(2017,6,30,23,0,0)
full_list = [base - datetime.timedelta(hours=x) for x in range(0, 24 * 547)]
full_list = [x for x in full_list if x.hour in [8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]]
sub_list = [x.to_pydatetime() for x in df_item['OptDate']]
dif_list = list(set(full_list) - set(sub_list))

# generate dataframe of missing date
df_dif = pd.DataFrame({'OptDate': dif_list})
df_dif['ItemCnt'] = [df_item[df_item['hour'] == x.hour]['ItemCnt'].mean() for x in df_dif['OptDate']]
df_dif['ItemCnt'] = df_dif['ItemCnt'].apply(lambda x: 0 if math.isnan(x) else x)
df_dif['ItemCnt'] = round(df_dif['ItemCnt'])

# concat two dataframes
df_item = pd.concat([df_item, df_dif])
df_item = df_item.sort_values(['OptDate'], ascending = [1])
df_item = df_item.reset_index(drop = True)
df_item = df_item[['OptDate', 'ItemCnt']]
df_item = df_item.set_index('OptDate')

# save data to file
df_item.to_csv(location + 'Output_Csv/' + itemName + '_hour.csv')
df_item.to_excel(location + 'Output_Xlsx/' + itemName + '_hour.xlsx')

# groupby 3 hours
df_item.index = df_item.index + datetime.timedelta(hours = 1)
df_item = df_item.groupby(pd.Grouper(freq='3H')).aggregate(np.sum)
df_item.index = df_item.index - datetime.timedelta(hours = 1)
df_item = df_item.dropna()

# winsorize data
tmp = scipy.stats.mstats.winsorize(df_item['ItemCnt'], limits=0.02).compressed()
tmp = pd.Series(tmp.tolist())
tmp.index = df_item['ItemCnt'].index
df_item['ItemCnt'] = tmp

# save data to file
df_item.to_csv(location + 'Output_Csv/' + itemName + '_3hour.csv')
df_item.to_excel(location + 'Output_Xlsx/' + itemName + '_3hour.xlsx')
