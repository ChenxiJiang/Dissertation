# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 16:51:11 2017

@author: cicijiang
"""
import config
import pandas as pd

# load config
location = config.location
shopNo = config.shopNo
itemNo = config.itemNo
itemName = config.itemName

df_3hour = pd.read_excel(location + 'Output_Xlsx/' + itemName + '_3hour.xlsx', index_col = 0)
df_day = pd.read_excel(location + 'Output_Xlsx/' + itemName + '_day.xlsx', index_col = 0)

# split df_3hour into train and test
train_size = int(len(df_3hour) * 0.8)
train, test = df_3hour[0:train_size], df_3hour[train_size:]

# save train and test into files
train.to_csv(location + 'Output_Csv/' + itemName + '_3hour_train.csv', header = True)
train.to_excel(location + 'Output_Xlsx/' + itemName + '_3hour_train.xlsx', header = True)
test.to_csv(location + 'Output_Csv/' + itemName + '_3hour_test.csv', header = True)
test.to_excel(location + 'Output_Xlsx/' + itemName + '_3hour_test.xlsx', header = True)

# split df_day into train and test
train_size = int(len(df_day) * 0.8)
train, test = df_day[0:train_size], df_day[train_size:]

# save train and test into files
train.to_csv(location + 'Output_Csv/' + itemName + '_day_train.csv', header = True)
train.to_excel(location + 'Output_Xlsx/' + itemName + '_day_train.xlsx', header = True)
test.to_csv(location + 'Output_Csv/' + itemName + '_day_test.csv', header = True)
test.to_excel(location + 'Output_Xlsx/' + itemName + '_day_test.xlsx', header = True)