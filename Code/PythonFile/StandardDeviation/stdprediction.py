import pandas as pd
import numpy as np
import sys
import datetime
import datetime as dt
import matplotlib.pyplot as plt
#import seaborn as sns

a = sys.argv[1]

b = datetime.datetime.strptime(a, '%d/%m/%Y %H:%M:%S')

time = b.time()
day = b.date().weekday()
if day ==6:
        day = day - 5
else:
        day = day + 2

h = time.hour
m = time.minute  
Time_index = h*60 + m
Time_index = Time_index/5

Day = 4
Time_index = 240


df=pd.read_csv("trainingdata.csv")
df.columns = ['Timestamp', 'PIR', 'Switch','Mobile']
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y %H:%M:%S')
df = df[(df['Switch']==1)]
df = df[(df['Mobile']==1)]
df = df.drop(['Switch', 'Mobile'], axis=1)
df = df.set_index('Timestamp')
data_fivemins = df.groupby(pd.Grouper(freq='5Min')).aggregate(np.sum)
data_fivemins = data_fivemins.reset_index(drop=False)
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
data_fivemins = data_fivemins[['Timestamp','Date','Time', 'Day','WDay','PIR']]
data_fivemins['Time_index'] = data_fivemins['Time'].dt.total_seconds().div(60).astype(int)
data_fivemins['Time_index'] = data_fivemins['Time_index'].div(5).astype(int)
data_fivemins = data_fivemins[['Timestamp','WDay','Time_index','PIR']]
data_fivemins = data_fivemins[(data_fivemins['PIR']==1)]

df_Sun = data_fivemins[data_fivemins['WDay'] == '1']
df_Mon = data_fivemins[data_fivemins['WDay'] == '2']
df_Tue = data_fivemins[data_fivemins['WDay'] == '3']
df_Wed = data_fivemins[data_fivemins['WDay'] == '4']
df_Thurs = data_fivemins[data_fivemins['WDay'] == '5']
df_Fri = data_fivemins[data_fivemins['WDay'] == '6']
df_Sat = data_fivemins[data_fivemins['WDay'] == '7']

Sun = df_Sun['Time_index']
Mon = df_Mon['Time_index']
Tue = df_Tue['Time_index']
Wed = df_Wed['Time_index']
Thurs = df_Thurs['Time_index']
Fri = df_Fri['Time_index']
Sat = df_Sat['Time_index']


Sun_mean, Sun_std = np.mean(Sun), np.std(Sun)
Mon_mean, Mon_std = np.mean(Mon), np.std(Mon)
Tue_mean, Tue_std = np.mean(Tue), np.std(Tue)
Wed_mean, Wed_std = np.mean(Wed), np.std(Wed)
Thurs_mean, Thurs_std = np.mean(Thurs), np.std(Thurs)
Fri_mean, Fri_std = np.mean(Fri), np.std(Fri)
Sat_mean, Sat_std = np.mean(Sat), np.std(Sat)

Sun_cut_off = Sun_std * 3
Mon_cut_off = Mon_std * 3
Tue_cut_off = Tue_std * 3
Wed_cut_off = Wed_std * 3
Thurs_cut_off = Thurs_std * 3
Fri_cut_off = Fri_std * 3
Sat_cut_off = Sat_std * 3


Sun_lower, Sun_upper = Sun_mean - Sun_cut_off, Sun_mean + Sun_cut_off
Mon_lower, Mon_upper = Mon_mean - Mon_cut_off, Mon_mean + Mon_cut_off
Tue_lower, Tue_upper = Tue_mean - Tue_cut_off, Tue_mean + Tue_cut_off
Wed_lower, Wed_upper = Wed_mean - Wed_cut_off, Wed_mean + Wed_cut_off
Thurs_lower, Thurs_upper = Thurs_mean - Thurs_cut_off, Thurs_mean + Thurs_cut_off
Fri_lower, Fri_upper = Fri_mean - Fri_cut_off, Fri_mean + Fri_cut_off
Sat_lower, Sat_upper = Sat_mean - Sat_cut_off, Sat_mean + Sat_cut_off

#if isinstance(Mon, pd.Series):
#    fig = sns.kdeplot(Mon, label = "Monday");
#if isinstance(Tue, pd.Series):
#    fig = sns.kdeplot(Tue, label = "Tuesday");
#if isinstance(Wed, pd.Series):
#    fig = sns.kdeplot(Wed, label = "Wednesday");
#if isinstance(Thurs, pd.Series):
#    fig = sns.kdeplot(Thurs, label = "Thursday");
#if isinstance(Fri, pd.Series):
#    fig = sns.kdeplot(Fri, label = "Friday");
#if isinstance(Sat, pd.Series):
#    fig = sns.kdeplot(Sat, label = "Saturday");
#if isinstance(Sun, pd.Series):
#    fig = sns.kdeplot(Sun, label = "Sunday");


#if isinstance(Mon, pd.Series):
#    fig = plt.hist(Mon, bins = 30, color='g', label='Monday');
#if isinstance(Tue, pd.Series):
#    fig = plt.hist(Tue, bins = 30, color='b', label='Tuesday');
#if isinstance(Wed, pd.Series):
#    fig = plt.hist(Wed, bins = 30, color='r', label='Wednesday');
#if isinstance(Thurs, pd.Series):
#    fig = plt.hist(Thurs, bins = 30, color='y', label='Thursday');
#if isinstance(Fri, pd.Series):
#    fig = plt.hist(Fri, bins = 30, color='c', label='Friday');
#if isinstance(Sat, pd.Series):
#    fig = plt.hist(Sat, bins = 30, color='k', label='Saturday');
#if isinstance(Sun, pd.Series):
#    fig = plt.hist(Sun, bins = 30, color='m', label='Sunday');


#fig.figure.savefig("datadistribution.png")

if (Day == 1):
    if (Time_index > Sun_upper or Time_index < Sun_lower):
        message="Chance of Intrusion"
    else:
        message = "At Peace"
        
if (Day == 2):
    if (Time_index > Mon_upper or Time_index < Mon_lower):
        message="Chance of Intrusion"
    else:
        message = "At Peace"
        
if (Day == 3):
    if (Time_index > Tue_upper or Time_index < Tue_lower):
        message="Chance of Intrusion"
    else:
        message = "At Peace"
        
if (Day == 4):
    if (Time_index > Wed_upper or Time_index < Wed_lower):
        message="Chance of Intrusion"
    else:
        message = "At Peace"
        
if (Day == 5):
    if (Time_index > Thurs_upper or Time_index < Thurs_lower):
        message="Chance of Intrusion"
    else:
        message = "At Peace"
        
if (Day == 6):
    if (Time_index > Fri_upper or Time_index < Fri_lower):
        message="Chance of Intrusion"
    else:
        message = "At Peace"
        
if (Day == 7):
    if (Time_index > Sat_upper or Time_index < Sat_lower):
        message="Chance of Intrusion"
    else:
        message = "At Peace"
        
print(message)

