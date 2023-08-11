#!/usr/bin/python
#--------------------------------------------------------------------- clock.py
# Display date and time as well as indoor and outdoor temperatures
# 
# (C) D Delmar Davis 2023 
#
# Note: POC lots of hard coded foo here....

import time
import subprocess
from board import SCL, SDA, D4
import busio
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1305

oled_reset = digitalio.DigitalInOut(D4)
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, reset=oled_reset)
disp.fill(0)
disp.show()

width = disp.width
height = disp.height
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "date +%X\ %d%b%y"
    TimeDate = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "fetchtemp.py"
    LocalTemp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'gathertemps.py'
    PromData = subprocess.check_output(cmd, shell=True).decode("utf-8")

    # Write four lines of text.

    draw.text((x, top + 0), "IP: " + IP, font=font, fill=255)
    draw.text((x, top + 8), TimeDate, font=font, fill=255)
    draw.text((x, top + 16), LocalTemp, font=font, fill=255)
    draw.text((x, top + 25), PromData, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.1)
