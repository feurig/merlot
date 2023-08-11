#!/usr/bin/python
#-----------------------------------------------------------------localtemps.py
# pull temperature sensor data from .prom file
# 
# (C) D Delmar Davis 2023 
#
# Note: POC lots of hard coded foo here....
with open('/var/lib/prometheus/node-exporter/temp.prom', 'r') as f:
    for line in f.readlines():
        if 'Xhome_temperature_farenheit' in ('X'+line) :
            print('%.2fF' % (float(line.split(' ')[1],)))
