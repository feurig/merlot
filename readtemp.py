#!/usr/bin/python
# should probly be some sort of  arguments for file name.
#
# */1 * * * * /usr/local/bin/readtemp.py

import sys
import board
import adafruit_tc74
import tempfile
import os
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_tc74.TC74(i2c)

tmpfile =os.path.join(tempfile.gettempdir(),'temp.prom')
print (tmpfile)

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
os.chmod(tmpfile, os.stat(tmpfile).st_mode | 0o111)
os.replace(tmpfile, '/var/lib/prometheus/node-exporter/temp.prom')
