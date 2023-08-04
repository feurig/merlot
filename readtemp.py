#!/usr/bin/python
# should probly be some sort of  arguments for file name.
#
# */1 * * * * /usr/local/bin/readtemp.py

import sys
import board
import adafruit_tc74
import adafruit_ahtx0
import tempfile
import os

i_can_has_temperature = False
i_can_has_humidity = False
temperature_read=0
humidity_read=0

i2c = board.I2C()  # uses board.SCL and board.SDA
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
    else:
        print ("found something else ", tempsensorid)

if (i_can_has_temperature):
    
    tmpfile =os.path.join(tempfile.gettempdir(),'temp.prom')

    #file = open('/var/lib/prometheus/node-exporter/temp.prom', 'w')
    file = open(tmpfile, 'w')
    sys.stdout = file
    print("# HELP home_temperature_farenheit Temperature read off of external sensor.")
    print("# TYPE home_temperature_farenheit gauge")
    print("home_temperature_farenheit %0.3f" % ((sensor.temperature * 1.8) + 32.0))
    print("# HELP home_temperature_celsius Temperature read off of external sensor.")
    print("# TYPE home_temperature_celsius gauge")
    print("ambient_temperature_celcius %0.3f" % sensor.temperature)
    if (i_can_has_humidity):
        print("# HELP home_relative_humidity Temperature read off of external sensor.")
        print("# TYPE home_relative_humidity gauge")
        print("home_relative_humidity %0.3f" % sensor.relative_humidity)
    file.close()
    os.replace(tmpfile, '/var/lib/prometheus/node-exporter/temp.prom')
