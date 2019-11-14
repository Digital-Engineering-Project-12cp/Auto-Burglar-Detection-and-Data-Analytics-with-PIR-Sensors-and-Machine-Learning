#!/bin/bash

python3 /home/manish/env/timestamp_formating.py
python3 /home/manish/env/timestamp_influxconversion_format.py
python3 /home/manish/env/timestamp_influx_lineprotocol_format.py

curl -i -XPOST 'http://localhost:8086/write?db=historicaldb' --data-binary @/home/manish/env/data_fivemins_new_line.txt
sudo rm -r /home/manish/env/datalog.csv
