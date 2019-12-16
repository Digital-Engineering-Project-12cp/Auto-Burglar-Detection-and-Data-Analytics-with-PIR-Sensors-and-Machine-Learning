import pandas as pd
import numpy as np
import datetime as dt

data=pd.read_csv("/home/manish/env/datalog.csv")
data.columns = ['Timestamp','PIR','Switch','Mobile']
data = data[['Timestamp','PIR','Switch','Mobile']]
data['Timestamp'] = pd.to_datetime(data['Timestamp'], format='%d/%m/%Y %H:%M:%S')
data = data.set_index('Timestamp')
d = {'PIR':'PIR','Switch':'Switch','Mobile':'Mobile'}
data = data.groupby(pd.Grouper(freq='5Min')).agg({'PIR':'sum','Switch': 'mean','Mobile':'mean'}).rename(columns=d)
data_fivemins = data.reset_index(drop=False)
data_fivemins = data_fivemins.replace(np.nan,0)

import math
def normal_round(n):
    if n - math.floor(n) < 0.5:
        return math.floor(n)
    return math.ceil(n)


data_fivemins['Switch']=data_fivemins['Switch'].apply(normal_round)
data_fivemins['Mobile']=data_fivemins['Mobile'].apply(normal_round)

data_fivemins['Day'] = data_fivemins['Timestamp'].dt.day_name()
data_fivemins.loc[data_fivemins.Day == 'Sunday', 'WDay'] = '1'
data_fivemins.loc[data_fivemins.Day == 'Monday', 'WDay'] = '2'
data_fivemins.loc[data_fivemins.Day == 'Tuesday', 'WDay'] = '3'
data_fivemins.loc[data_fivemins.Day == 'Wednesday', 'WDay'] = '4'
data_fivemins.loc[data_fivemins.Day == 'Thursday', 'WDay'] = '5'
data_fivemins.loc[data_fivemins.Day == 'Friday', 'WDay'] = '6'
data_fivemins.loc[data_fivemins.Day == 'Saturday', 'WDay'] = '7'
data_fivemins['Timestamp'] = data_fivemins['Timestamp'].astype(str)
data_fivemins[['Date','Time']] = data_fivemins.Timestamp.str.split(" ",expand=True)
data_fivemins['Time'] = pd.to_timedelta(data_fivemins['Time'], unit='s')
data_fivemins = data_fivemins[['Timestamp','Date','Time', 'Day','WDay','PIR','Switch','Mobile']]
data_fivemins['Time_index'] = data_fivemins['Time'].dt.total_seconds().div(60).astype(int)
data_fivemins['Time_index'] = data_fivemins['Time_index'].div(5).astype(int)
data_fivemins_reqd = data_fivemins[['Timestamp','WDay','Time_index','PIR','Switch','Mobile']]

data_fivemins_reqd.to_csv ('/home/manish/env/data_fiveminsnew.csv', index = False, header=True) 
