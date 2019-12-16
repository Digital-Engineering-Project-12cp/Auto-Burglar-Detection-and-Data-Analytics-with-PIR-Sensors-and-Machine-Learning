import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

df=pd.read_csv("/home/manish/env/trainingdata.csv")
df.columns = ['Timestamp', 'PIR', 'Switch','Mobile']
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y %H:%M:%S')
df = df.drop(['Switch', 'Mobile'], axis=1)

weeks = [g for n, g in df.groupby(pd.Grouper(key='Timestamp',freq='W'))]
i=0
df={}
for i in range(0,len(weeks)):
    df[i] = pd.DataFrame()
    df[i] = weeks[i]
    df[i] = df[i].set_index('Timestamp')
    df[i] = df[i].groupby(pd.Grouper(freq='5Min')).aggregate(np.sum)
    df[i] = df[i].reset_index(drop=False)
    df[i]['Day'] = df[i]['Timestamp'].dt.day_name()
    df[i].loc[df[i].Day == 'Sunday', 'WDay'] = '1' 
    df[i].loc[df[i].Day == 'Monday', 'WDay'] = '2' 
    df[i].loc[df[i].Day == 'Tuesday', 'WDay'] = '3' 
    df[i].loc[df[i].Day == 'Wednesday', 'WDay'] = '4' 
    df[i].loc[df[i].Day == 'Thursday', 'WDay'] = '5' 
    df[i].loc[df[i].Day == 'Friday', 'WDay'] = '6' 
    df[i].loc[df[i].Day == 'Saturday', 'WDay'] = '7'
    df[i]['Timestamp'] = df[i]['Timestamp'].astype(str)
    df[i][['Date','Time']] = df[i].Timestamp.str.split(" ",expand=True)
    df[i]['Time'] = pd.to_timedelta(df[i]['Time'], unit='s')
    df[i] = df[i][['Timestamp','Date','Time', 'Day','WDay','PIR']]
    df[i]['Time_index'] = df[i]['Time'].dt.total_seconds().div(60).astype(int)
    df[i]['Time_index'] = df[i]['Time_index'].div(5).astype(int)
    df[i]['Timestamp'] = pd.to_datetime(df[i]['Timestamp'], format='%Y-%m-%d %H:%M:%S')
    df[i] = df[i][(df[i]['PIR']==1)]
    if i == 0:
        fig = df[i].boxplot(by="Day", column="Time_index",showfliers=True,showmeans=True,meanline=True)
        plt.title("First week detections")
        plt.suptitle("")
        fig.figure.savefig("/home/manish/env/images/firstweekdetectedtimestamps.png")
    if i == 1:
        fig = df[i].boxplot(by="Day", column="Time_index",showfliers=True,showmeans=True,meanline=True)
        plt.title("Second week detections")
        plt.suptitle("")
        fig.figure.savefig("/home/manish/env/images/secondweekdetectedtimestamps.png")
    if i==2:
        fig = df[i].boxplot(by="Day", column="Time_index",showfliers=True,showmeans=True,meanline=True)
        plt.title("Third  week detections")
        plt.suptitle("")
        fig.figure.savefig("/home/manish/env/images/thirdweekdetectedtimestamps.png")
    if i==3:
        fig = df[i].boxplot(by="Day", column="Time_index",showfliers=True,showmeans=True,meanline=True)
        plt.title("Fourth  week detections")
        plt.suptitle("")
        fig.figure.savefig("/home/manish/env/images/fourthweekdetectedtimestamps.png")


