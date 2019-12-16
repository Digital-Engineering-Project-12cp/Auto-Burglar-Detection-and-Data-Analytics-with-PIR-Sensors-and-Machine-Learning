from influxdb import InfluxDBClient
import pandas as pd
import numpy as np
import sys
import datetime
import json


#print(len(sys.argv))
#print(sys.argv[1])
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
Time_index = round(Time_index/5)
Time_index = Time_index - 1
#print ( Time_index) 2
#print(Time_index_min)
#print(Time_index_max)

Mobile_Mac = 1
Switch_Val = 1

client = InfluxDBClient(host='localhost', port=8086)

params ={"day":day,"Time_index" : Time_index, "Mobile_Mac":Mobile_Mac,"Switch_Val":Switch_Val}


#Result = client.query('SELECT MEAN("PIR") FROM "motionsensor5min"."autogen"."sensor" WHERE "WDay" = $day  AND "Time_index" >= $Time_index_min  AND "Time_index" <= $Time_index_max ')
Result = client.query('select SUM(PIR) from "historicaldb"."autogen"."sensor" ' 'where WDay=$day ' 'and Mobile =$Mobile_Mac ' 'and Time_index =$Time_index ' 'and Switch =$Switch_Val ', params={"params":json.dumps(params)})
Result1 = client.query('select COUNT(WDay) from "historicaldb"."autogen"."sensor" ' 'where WDay=$day ' 'and Mobile =$Mobile_Mac ' 'and Time_index =$Time_index ' 'and Switch =$Switch_Val ', params={"params":json.dumps(params)})

dd = []
qq = []

points = Result.get_points()
for point in points:
        dd.append(point['sum'])


points1 = Result1.get_points()
for point in points1:
         qq.append(point['count'])



print (dd[0]/qq[0])

