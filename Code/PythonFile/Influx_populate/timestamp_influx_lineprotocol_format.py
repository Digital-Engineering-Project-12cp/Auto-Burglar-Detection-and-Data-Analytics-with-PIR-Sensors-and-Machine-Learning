import pandas as pd
maindata = pd.read_csv("/home/manish/env/data_fivemins_new_influx.csv")
maindata["Timestamp"] = [str(maindata["Timestamp"][t]) + "000000000" for t in range(len(maindata))]
lines = ["sensor"
         + ",type=motion"
         + " "
         + "WDay=" + str(maindata["WDay"][d])
         + ","
         + "Time_index=" + str(maindata["Time_index"][d])
         + ","
         +"PIR=" + str(maindata["PIR"][d])
         + ","
         +"Switch=" + str(maindata["Switch"][d])
         + ","
         +"Mobile=" + str(maindata["Mobile"][d])
         + " " + str(maindata["Timestamp"][d]) for d in range(len(maindata))]
thefile = open("/home/manish/env/data_fivemins_new_line.txt", 'w')
for item in lines:
    thefile.write("%s\n" % item)
