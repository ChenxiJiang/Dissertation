# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 00:25:45 2017

@author: cicijiang
"""
import config
import pandas as pd
import datetime

# load config
location = config.location

def convert_excel_date(excel_date):
    return datetime.datetime.fromordinal(datetime.datetime(1900, 1, 1).toordinal() + excel_date - 2)

# load data
df = pd.read_excel(location + 'Output_Xlsx/weather_original.xlsx', header = 0)
df.columns = ['Date', 'Weather', 'Temperture', 'Wind']
df['Date'] = df['Date'].apply(lambda x: convert_excel_date(x).date())

# seperate columns
df_weather = df['Weather'].str.get_dummies(sep='/')
df_weather.columns = ['-', 'RainHeavy', 'RainHeavy', 'Cloudy', 'Cloudy', 'RainHeavy', 'RainHeavy', 'RainLight', 'RainLight', 'Snow', 'Sunny', 'Sunny', 'RainHeavy', 'RainHeavy', 'Cloudy', 'Cloudy', 'RainLight', 'RainLight', 'RainLight']
df_weather = df_weather.groupby(df_weather.columns, axis=1).sum()
df_weather = df_weather.replace(2,1)

df = pd.concat([df,df_weather], axis = 1)
df = df.drop(['-', 'Weather', 'Temperture', 'Wind'], axis = 1)

#save data to file
df.to_excel(location + 'Output_Xlsx/weather.xlsx')