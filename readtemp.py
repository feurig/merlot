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

GotTemperature = False
GotHumidity = False
TempRead=0
HumidityRead=0

i2c = board.I2C()  # uses board.SCL and board.SDA
for tempsensorid in i2c.scan():
    if (tempsensorid==72):
        print ("found a TC74")
        sensor = adafruit_tc74.TC74(i2c)
        TempRead=sensor.temperature
        GotTemperature = True
    if (tempsensorid==38):
        print ("found an AHTx0")
        sensor = adafruit_ahtx0.AHTx0(i2c)
        TempRead=sensor.temperature
        GotTemperature = True
        HumidityRead = sensor.relative_humidity

if (GotTemperature):
    
    tmpfile =os.path.join(tempfile.gettempdir(),'temp.prom')

    #file = open('/var/lib/prometheus/node-exporter/temp.prom', 'w')
    file = open(tmpfile, 'w')
    sys.stdout = file
    print("# HELP ambient_temperature_farenheit Temperature read off of external sensor.")
    print("# TYPE ambient_temperature_farenheit gauge")
    print("ambient_temperature_farenheit{type=\"backyard\"} %0.3f" % ((sensor.temperature * 1.8) + 32.0))
    print("# HELP ambient_temperature_celsius Temperature read off of external sensor.")
    print("# TYPE ambient_temperature_celsius gauge")
    print("ambient_temperature_celcius{type=\"backyard\"} %0.3f" % sensor.temperature)
    file.close()
    os.replace(tmpfile, '/var/lib/prometheus/node-exporter/temp.prom')
