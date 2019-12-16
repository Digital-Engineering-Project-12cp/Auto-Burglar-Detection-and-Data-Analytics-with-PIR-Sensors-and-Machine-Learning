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
#print ( Time_index)
#Time_index_min = Time_index - 1
#Time_index_max = Time_index + 1
#print(Time_index_min)
#print(Time_index_max)


client = InfluxDBClient(host='localhost', port=8086)

params ={"day":day,"Time_index" : Time_index }


#Result = client.query('SELECT MEAN("PIR") FROM "historicaldb"."autogen"."sensor" WHERE "WDay" = $day  AND "Time_index" >= $Time_index_min  AND "Time_index" <= $Time_index_max ')
Result = client.query('select SUM(PIR) from "historicaldb"."autogen"."sensor" ' 'where WDay=$day ' 'and Time_index =$Time_index ' , params={"params":json.dumps(params)})
Result1 = client.query('select COUNT(WDay) from "historicaldb"."autogen"."sensor" ' 'where WDay=$day ' 'and Time_index =$Time_index ' , params={"params":json.dumps(params)})

dd = []
qq = []

points = Result.get_points()
for point in points:
        dd.append(point['sum'])


points1 = Result1.get_points()
for point in points1:
         qq.append(point['count'])



print (dd[0]/qq[0])


#        kopp = point['mean']
#print(kopp)
