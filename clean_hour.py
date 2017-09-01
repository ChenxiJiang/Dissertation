#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 23:39:28 2017

@author: cicijiang
"""
import config
import pandas as pd
import datetime

# load config
location = config.location
shopNo = config.shopNo

# read excel
df = pd.read_excel(location + 'Output_Xlsx/items_hour.xlsx')

# select shop
df = df[df['ShopNo'] == shopNo]
df['OptDate'] = pd.to_datetime(df['OptDate'])
df['OptDate'] = df['OptDate'].apply(lambda x: x + datetime.timedelta(hours=1) if x.hour == 7 else x)
df['OptDate'] = df['OptDate'].apply(lambda x: x - datetime.timedelta(hours=1) if x.hour == 23 else x)

# groupby 'ShopNo', 'ItemName', 'OptDate', 'ItemNo'
df = df.groupby(['ShopNo', 'ItemName', 'OptDate', 'ItemNo']).agg({'ItemCnt': 'sum'}).reset_index()

# save data to file
df.to_excel(location + 'Output_Xlsx/items_hour_' + str(shopNo) + '.xlsx')

# groupby 'ItemName',  'ItemNo'
df = df.groupby(['ItemName', 'ItemNo']).agg({'ItemCnt': 'sum'}).reset_index()

# calculate percentage of six items
t = df['ItemCnt'].sum()
s = df[(df['ItemNo'] == 10401123) | (df['ItemNo'] == 10401144) | (df['ItemNo'] == 10401169) | (df['ItemNo'] == 10401141) | (df['ItemNo'] == 10403012) | (df['ItemNo'] == 10401091)]['ItemCnt'].sum()
p = s/t

# save data to txt
with open(location + '/Predictions/describe_2102.txt', 'w') as f:
    f.write("total items: %d\n" % t)
    f.write("sum of six items: %d\n" % s)
    f.write("sum of six items percentage: %f" % p)