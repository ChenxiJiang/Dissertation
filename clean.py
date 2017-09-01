#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 17:58:35 2017

@author: cicijiang
"""
import config
import pandas as pd
import datetime
import os

# load config
location = config.location

files = os.listdir(location + 'Data')
#files.remove('.DS_Store');
df_all = pd.DataFrame()
for file in files:
    print("Cleaning file " + file)
    df = pd.read_excel(location + 'Data/' + file)
    df = df[df['ShopNo'] == 2102]
    #drop column
    df = df.drop(['WholeDisc','Operator','Payed','SettleID','TicketSpare',
                  'FavorAmt','CstName','CstPhone','MemoStr','FinCardNo',
                  'FinCardPayed','FinCashPayed','FinTicketPayed','FinTicketSpare',
                  'FinPayAmt','FinDate','GuideNo'], axis = 1)
    
    # Split 'ButDetail' and store in multiple rows
    item = df['ButDetail'].str.split(';').apply(pd.Series, 1).stack()
    item.index = item.index.droplevel(-1)
    item.name = 'Item'
    df = df.join(item).reset_index()
    df = df.drop(df[df['Item'] == ''].index)
    df = df.drop(['index', 'ButDetail'], axis = 1)
    
    # Split 'Item' and store in new columns
    df = df[df['Item'].notnull()]
    df = df.join(df['Item'].apply(lambda x: pd.Series(x.split(','))))
    df = df.drop(['Item', 13], axis = 1)
    
    # Groupby
    df = df.rename(columns = {0:'ItemNo',1:'ItemName',2:'ItemUnit',3:'Price',4:'Rate',5:'ItemCnt',6:'ItemSum',7:'IsSpecialPrice',8:'IsMemberPrice',9:'IsTimeDisc',10:'IsReturns',11:'TicketRec',12:'TicketArr'})
    df = df.drop(df[df['ItemName'] == ''].index)
    
    # convert string to integer, then 1+1 = 2,otherwise 1+1 = 11
    df['ItemCnt'] = df['ItemCnt'].astype(int)
    
    # convert string to datetime and set minute, second to 0
    df['OptDate'] = df['OptDate'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S") if type(x) == str else x)
    df['OptDate'] = df['OptDate'].apply(lambda x: x.replace(minute = 0, second = 0))
    
    # select one product and count its daily amount in different store 
    df_item_104 = df[df['ItemNo'].str.startswith("104")]
    df_all = df_all.append(df_item_104)
    
# group by hour and save to xlsx
df_hour = df_all.groupby(['ShopNo', 'ItemName', 'OptDate', 'ItemNo']).agg({'ItemCnt': 'sum'}).reset_index()
df_hour.to_excel(location + 'Output_Xlsx/items_hour.xlsx')

# group by day
df_all['OptDate'] = df_all['OptDate'].apply(lambda x: x.replace(hour = 0))
df_day = df_all.groupby(['ShopNo', 'ItemName', 'OptDate', 'ItemNo']).agg({'ItemCnt': 'sum'}).reset_index()

# count item sold days and save to xlsx
df_count = df_day.groupby(['ShopNo', 'ItemName', 'ItemNo']).count().reset_index()
df_count = df_count.drop(['OptDate'], axis = 1)
df_count = df_count.rename(columns = {'ItemCnt': 'DayCount'})
df_count = df_count.sort_values(by = ['DayCount'], ascending=[0])
df_count.to_excel(location + 'Output_Xlsx/items_day_count_original.xlsx')