#!/usr/bin/python
#-------------------------------------------------------------------readtemp.py
#
#  detect i2c temperature sensor read it and put its data where node_exporter
#  will send it to prometheus.
# 
# (C) D Delmar Davis 2023 
#
# Note: POC lots of hard coded foo here....
# should probly be some sort of  arguments for file name.
# your crontab should look like this
# */1 * * * * /usr/local/bin/readtemp.py

import sys
import board
import adafruit_tc74
import adafruit_ahtx0
import adafruit_sht4x
from adafruit_dps310.basic import DPS310
import tempfile
import os

i_can_has_temperature = False
i_can_has_humidity = False
i_can_has_pressure = False
temperature_read=0
humidity_read=0
pressure_read=0

i2c = board.I2C()  # uses board.SCL and board.SDA
print(i2c.scan())
for tempsensorid in i2c.scan():
    if (tempsensorid==72):
        print ("found a TC74")
        sensor = adafruit_tc74.TC74(i2c)
        temperature_read=sensor.temperature
        i_can_has_temperature = True
    elif (tempsensorid==56):
        print ("found an AHTx0")
        sensor = adafruit_ahtx0.AHTx0(i2c)
        temperature_read=sensor.temperature
        i_can_has_temperature = True
        humidity_read = sensor.relative_humidity
        i_can_has_humidity = True
    elif (False): #tempsensorid==44):
        print ("found an SHT4x")
        sensor = adafruit_sht4x.SHT4x(board.I2C())
        temperature_read=sensor.temperature
        i_can_has_temperature = True
        humidity_read = sensor.relative_humidity
        i_can_has_humidity = True
    elif (tempsensorid==119):
        print ("found a EPS310")
        sensor = DPS310(i2c)
        temperature_read=sensor.temperature
        i_can_has_temperature = True
        pressure_read = sensor.pressure
        i_can_has_pressure = True
    else:
        print ("found something else ", tempsensorid)

if (i_can_has_temperature):
    
    tmpfile =os.path.join(tempfile.gettempdir(),'temp.prom')

    #file = open('/var/lib/prometheus/node-exporter/temp.prom', 'w')
    file = open(tmpfile, 'w')
    sys.stdout = file
    print("# HELP home_temperature_farenheit Temperature read off of external sensor.")
    print("# TYPE home_temperature_farenheit gauge")
    print("home_temperature_farenheit %0.3f" % ((temperature_read * 1.8) + 32.0))
    print("# HELP home_temperature_celsius Temperature read off of external sensor.")
    print("# TYPE home_temperature_celsius gauge")
    print("home_temperature_celcius %0.3f" % temperature_read)
    if (i_can_has_humidity):
        print("# HELP home_relative_humidity Temperature read off of external sensor.")
        print("# TYPE home_relative_humidity gauge")
        print("home_relative_humidity %0.3f" % humidity_read)
    if (i_can_has_pressure):
        print("# HELP home_barometric_pressure Barometric Pressure read off of external sensor.")
        print("# TYPE home_barometric_pressure gauge")
        print("home_barometric_pressure %0.3f" % pressure_read)
    file.close()
    os.replace(tmpfile, '/var/lib/prometheus/node-exporter/temp.prom')
