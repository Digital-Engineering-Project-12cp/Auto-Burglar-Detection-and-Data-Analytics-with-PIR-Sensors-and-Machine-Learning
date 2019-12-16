import pandas as pd
import numpy as np
import sys
import datetime
import datetime as dt
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

a = sys.argv[1]
#print(a)
b = datetime.datetime.strptime(a, '%d/%m/%Y %H:%M:%S')

time = b.time()
day = b.date().weekday()
if day ==6:
        day = day - 5
else:
        day = day + 2
#print (day)
#print(time)
h = time.hour
m = time.minute  
Time_index = h*60 + m
Time_index = Time_index/5
#print ( Time_index)
# Time_index_min = Time_index - 1
# Time_index_max = Time_index + 1
#print(Time_index_min)

df=pd.read_csv("trainingdata.csv")
df.columns = ['Timestamp', 'PIR', 'Switch','Mobile']
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%d/%m/%Y %H:%M:%S')
df = df[(df['Switch']==1)]
df = df[(df['Mobile']==1)]
df = df.drop(['Switch', 'Mobile'], axis=1)
days = [g for n, g in df.groupby(pd.Grouper(key='Timestamp',freq='D'))]

i=0
df={}

Mon_median_list = []
Mon_upper_quartile_list = []
Mon_lower_quartile_list = []
Mon_iqr_list = []
Mon_upper_whisker_list = []
Mon_lower_whisker_list = []

Tue_median_list = []
Tue_upper_quartile_list = []
Tue_lower_quartile_list = []
Tue_iqr_list = []
Tue_upper_whisker_list = []
Tue_lower_whisker_list = []

Wed_median_list = []
Wed_upper_quartile_list = []
Wed_lower_quartile_list = []
Wed_iqr_list = []
Wed_upper_whisker_list = []
Wed_lower_whisker_list = []

Thurs_median_list = []
Thurs_upper_quartile_list = []
Thurs_lower_quartile_list = []
Thurs_iqr_list = []
Thurs_upper_whisker_list = []
Thurs_lower_whisker_list = []

Fri_median_list = []
Fri_upper_quartile_list = []
Fri_lower_quartile_list = []
Fri_iqr_list = []
Fri_upper_whisker_list = []
Fri_lower_whisker_list = []

Sat_median_list = []
Sat_upper_quartile_list = []
Sat_lower_quartile_list = []
Sat_iqr_list = []
Sat_upper_whisker_list = []
Sat_lower_whisker_list = []

Sun_median_list = []
Sun_upper_quartile_list = []
Sun_lower_quartile_list = []
Sun_iqr_list = []
Sun_upper_whisker_list = []
Sun_lower_whisker_list = []


for i in range(0,len(days)):
    df[i] = pd.DataFrame()
    df[i] = days[i]
    if not df[i].empty:
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
        median = np.median(df[i]['Time_index'])
        if not df[i]['Time_index'].empty:
            upper_quartile = np.percentile(df[i]['Time_index'], 75)
            lower_quartile = np.percentile(df[i]['Time_index'], 25)
            iqr = upper_quartile - lower_quartile
            upper_whisker = df[i]['Time_index'][df[i]['Time_index']<=upper_quartile+1.5*iqr].max()
            lower_whisker = df[i]['Time_index'][df[i]['Time_index']>=lower_quartile-1.5*iqr].min()
#             print(df[i].Day.mode())
#             print("median=", median)
#             print("upper_quartile = ", upper_quartile)
#             print("lower_quartile = ", lower_quartile)
#             print("iqr= ",iqr)
#             print("upper_whisker= ", upper_whisker)
#             print("lower_whisker= ", lower_whisker)
           
            if df[i]['Day'].str.contains('Monday').any():
                Mon_median_list.append(median)
                Mon_upper_quartile_list.append(upper_quartile)
                Mon_lower_quartile_list.append(lower_quartile)
                Mon_upper_whisker_list.append(upper_whisker)
                Mon_lower_whisker_list.append(lower_whisker)
                Mon_iqr_list.append(iqr)
#                 print(Mon_median_list)
#                 print(Mon_upper_quartile_list)
#                 print(Mon_lower_quartile_list)
#                 print(Mon_upper_whisker_list)
#                 print(Mon_lower_whisker_list)
#                 print(Mon_iqr_list)
                Mon_median_list_mean = np.mean(Mon_median_list)
                Mon_upper_quartile_list_mean = np.mean(Mon_upper_quartile_list)
                Mon_lower_quartile_list_mean = np.mean(Mon_lower_quartile_list)
                Mon_upper_whisker_list_mean = np.mean(Mon_upper_whisker_list)
                Mon_lower_whisker_list_mean = np.mean(Mon_lower_whisker_list)
                Mon_iqr_list_mean = np.mean(Mon_iqr_list)
                if (Time_index > (Mon_upper_quartile_list_mean + 3*Mon_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index < (Mon_lower_quartile_list_mean - 3*Mon_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index > (Mon_upper_quartile_list_mean + 1.5*Mon_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                elif (Time_index < (Mon_lower_quartile_list_mean - 1.5*Mon_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                else :
                	message = "At Peace"

                
                
            if df[i]['Day'].str.contains('Tuesday').any():
                Tue_median_list.append(median)
                Tue_upper_quartile_list.append(upper_quartile)
                Tue_lower_quartile_list.append(lower_quartile)
                Tue_upper_whisker_list.append(upper_whisker)
                Tue_lower_whisker_list.append(lower_whisker)
                Tue_iqr_list.append(iqr)
#                 print(Tue_median_list)
#                 print(Tue_upper_quartile_list)
#                 print(Tue_lower_quartile_list)
#                 print(Tue_upper_whisker_list)
#                 print(Tue_lower_whisker_list)
#                 print(Tue_iqr_list)
                Tue_median_list_mean = np.mean(Tue_median_list)
                Tue_upper_quartile_list_mean = np.mean(Tue_upper_quartile_list)
                Tue_lower_quartile_list_mean = np.mean(Tue_lower_quartile_list)
                Tue_upper_whisker_list_mean = np.mean(Tue_upper_whisker_list)
                Tue_lower_whisker_list_mean = np.mean(Tue_lower_whisker_list)
                Tue_iqr_list_mean = np.mean(Tue_iqr_list)
                if (Time_index > (Tue_upper_quartile_list_mean + 3*Tue_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index < (Tue_lower_quartile_list_mean - 3*Tue_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index > (Tue_upper_quartile_list_mean + 1.5*Tue_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                elif (Time_index < (Tue_lower_quartile_list_mean - 1.5*Tue_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                else :
                	message = "At Peace"
                
            if df[i]['Day'].str.contains('Wednesday').any():
                Wed_median_list.append(median)
                Wed_upper_quartile_list.append(upper_quartile)
                Wed_lower_quartile_list.append(lower_quartile)
                Wed_upper_whisker_list.append(upper_whisker)
                Wed_lower_whisker_list.append(lower_whisker)
                Wed_iqr_list.append(iqr)
#                 print(Wed_median_list)
#                 print(Wed_upper_quartile_list)
#                 print(Wed_lower_quartile_list)
#                 print(Wed_upper_whisker_list)
#                 print(Wed_lower_whisker_list)
#                 print(Wed_iqr_list)
                Wed_median_list_mean = np.mean(Wed_median_list)
                Wed_upper_quartile_list_mean = np.mean(Wed_upper_quartile_list)
                Wed_lower_quartile_list_mean = np.mean(Wed_lower_quartile_list)
                Wed_upper_whisker_list_mean = np.mean(Wed_upper_whisker_list)
                Wed_lower_whisker_list_mean = np.mean(Wed_lower_whisker_list)
                Wed_iqr_list_mean = np.mean(Wed_iqr_list)
                if (Time_index > (Wed_upper_quartile_list_mean + 3*Wed_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index < (Wed_lower_quartile_list_mean - 3*Wed_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index > (Wed_upper_quartile_list_mean + 1.5*Wed_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                elif (Time_index < (Wed_lower_quartile_list_mean - 1.5*Wed_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                else :
                	message = "At Peace"
                
                
            if df[i]['Day'].str.contains('Thursday').any():
                Thurs_median_list.append(median)
                Thurs_upper_quartile_list.append(upper_quartile)
                Thurs_lower_quartile_list.append(lower_quartile)
                Thurs_upper_whisker_list.append(upper_whisker)
                Thurs_lower_whisker_list.append(lower_whisker)
                Thurs_iqr_list.append(iqr)
#                 print(Thurs_median_list)
#                 print(Thurs_upper_quartile_list)
#                 print(Thurs_lower_quartile_list)
#                 print(Thurs_upper_whisker_list)
#                 print(Thurs_lower_whisker_list)
#                 print(Thurs_iqr_list)
                Thurs_median_list_mean = np.mean(Thurs_median_list)
                Thurs_upper_quartile_list_mean = np.mean(Thurs_upper_quartile_list)
                Thurs_lower_quartile_list_mean = np.mean(Thurs_lower_quartile_list)
                Thurs_upper_whisker_list_mean = np.mean(Thurs_upper_whisker_list)
                Thurs_lower_whisker_list_mean = np.mean(Thurs_lower_whisker_list)
                Thurs_iqr_list_mean = np.mean(Thurs_iqr_list)
                if (Time_index > (Thurs_upper_quartile_list_mean + 3*Thurs_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index < (Thurs_lower_quartile_list_mean - 3*Thurs_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index > (Thurs_upper_quartile_list_mean + 1.5*Thurs_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                elif (Time_index < (Thurs_lower_quartile_list_mean - 1.5*Thurs_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                else :
                	message = "At Peace"
                
            if df[i]['Day'].str.contains('Friday').any():
                Fri_median_list.append(median)
                Fri_upper_quartile_list.append(upper_quartile)
                Fri_lower_quartile_list.append(lower_quartile)
                Fri_upper_whisker_list.append(upper_whisker)
                Fri_lower_whisker_list.append(lower_whisker)
                Fri_iqr_list.append(iqr)
#                 print(Fri_median_list)
#                 print(Fri_upper_quartile_list)
#                 print(Fri_lower_quartile_list)
#                 print(Fri_upper_whisker_list)
#                 print(Fri_lower_whisker_list)
#                 print(Fri_iqr_list)
                Fri_median_list_mean = np.mean(Fri_median_list)
                Fri_upper_quartile_list_mean = np.mean(Fri_upper_quartile_list)
                Fri_lower_quartile_list_mean = np.mean(Fri_lower_quartile_list)
                Fri_upper_whisker_list_mean = np.mean(Fri_upper_whisker_list)
                Fri_lower_whisker_list_mean = np.mean(Fri_lower_whisker_list)
                Fri_iqr_list_mean = np.mean(Fri_iqr_list)
                if (Time_index > (Fri_upper_quartile_list_mean + 3*Fri_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index < (Fri_lower_quartile_list_mean - 3*Fri_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index > (Fri_upper_quartile_list_mean + 1.5*Fri_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                elif (Time_index < (Fri_lower_quartile_list_mean - 1.5*Fri_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                else :
                	message = "At Peace"
                
            if df[i]['Day'].str.contains('Saturday').any():
                Sat_median_list.append(median)
                Sat_upper_quartile_list.append(upper_quartile)
                Sat_lower_quartile_list.append(lower_quartile)
                Sat_upper_whisker_list.append(upper_whisker)
                Sat_lower_whisker_list.append(lower_whisker)
                Sat_iqr_list.append(iqr)
#                 print(Sat_median_list)
#                 print(Sat_upper_quartile_list)
#                 print(Sat_lower_quartile_list)
#                 print(Sat_upper_whisker_list)
#                 print(Sat_lower_whisker_list)
#                 print(Sat_iqr_list)
                Sat_median_list_mean = np.mean(Sat_median_list)
                Sat_upper_quartile_list_mean = np.mean(Sat_upper_quartile_list)
                Sat_lower_quartile_list_mean = np.mean(Sat_lower_quartile_list)
                Sat_upper_whisker_list_mean = np.mean(Sat_upper_whisker_list)
                Sat_lower_whisker_list_mean = np.mean(Sat_lower_whisker_list)
                Sat_iqr_list_mean = np.mean(Sat_iqr_list)
                if (Time_index > (Sat_upper_quartile_list_mean + 3*Sat_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index < (Sat_lower_quartile_list_mean - 3*Sat_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index > (Sat_upper_quartile_list_mean + 1.5*Sat_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                elif (Time_index < (Sat_lower_quartile_list_mean - 1.5*Sat_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                else :
                	message = "At Peace"
                
            if df[i]['Day'].str.contains('Sunday').any():
                Sun_median_list.append(median)
                Sun_upper_quartile_list.append(upper_quartile)
                Sun_lower_quartile_list.append(lower_quartile)
                Sun_upper_whisker_list.append(upper_whisker)
                Sun_lower_whisker_list.append(lower_whisker)
                Sun_iqr_list.append(iqr)
#                 print(Sun_median_list)
#                 print(Sun_upper_quartile_list)
#                 print(Sun_lower_quartile_list)
#                 print(Sun_upper_whisker_list)
#                 print(Sun_lower_whisker_list)
#                 print(Sun_iqr_list)
                Sun_median_list_mean = np.mean(Sun_median_list)
                Sun_upper_quartile_list_mean = np.mean(Sun_upper_quartile_list)
                Sun_lower_quartile_list_mean = np.mean(Sun_lower_quartile_list)
                Sun_upper_whisker_list_mean = np.mean(Sun_upper_whisker_list)
                Sun_lower_whisker_list_mean = np.mean(Sun_lower_whisker_list)
                Sun_iqr_list_mean = np.mean(Sun_iqr_list)
                if (Time_index > (Sun_upper_quartile_list_mean + 3*Sun_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index < (Sun_lower_quartile_list_mean - 3*Sun_iqr_list_mean)):
                	message = "More probable Intrusion Chance"
                elif (Time_index > (Sun_upper_quartile_list_mean + 1.5*Sun_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                elif (Time_index < (Sun_lower_quartile_list_mean - 1.5*Sun_iqr_list_mean)):
                	message = "Less probable Intrusion Chance"
                else :
                	message = "At Peace"

print(message)
                
                                
