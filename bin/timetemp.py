#!/usr/bin/python3
# References : SPDX-FileCopyrightText: 2019 Mikey Sklar for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board # type: ignore
import busio # type: ignore

hat_id_file_path = "/proc/device-tree/hat/product"
hat_is_a_rainbow_hat = False

try:
    file=open(hat_id_file_path, "r") 
    content = "" 
    for line in file.readlines():
       content += line
    print(content) 
    if ('Rainbow HAT' in content):
       hat_is_a_rainbow_hat = True
except FileNotFoundError:
    print("The file was not found. Please check the path.")
    
print("'Rainbow HAT'?" + str(hat_is_a_rainbow_hat) )

from adafruit_ht16k33 import segments # type: ignore

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = segments.Seg7x4(i2c)

# Clear the display.
display.fill(0)
while True:
    display.print(time.strftime("%H:%M"))
    time.sleep(5)
    file=open('/var/lib/prometheus/node-exporter/temp.prom')
    display.colon = False
    for line in file.readlines():
        values=line.split()[0:2]
        if values[0]=='home_temperature_farenheit':
            display.print(str(values[1])[0:4]+'f')
    file.close()
    time.sleep(5)
    
