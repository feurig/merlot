#!/usr/bin/python3
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
from datetime import datetime
import math
import atexit
import signal


oled_reset = digitalio.DigitalInOut(D4)
i2c = busio.I2C(SCL, SDA)
disp = adafruit_ssd1305.SSD1305_I2C(128, 32, i2c, reset=oled_reset)
disp.poweron()
disp.fill(0)
disp.show()
displayIsOff=False 

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

def draw_clock(t: datetime):
    ctop=top+3
    cbottom=bottom-1
    center=(cbottom-ctop)/2
    h=t.hour
    m=t.minute
    ml = center * 0.9 #fix later
    hl = center * 0.6
    a = 90.0 - (m / 60.0) * 360.0
    r = a * math.pi / 180.0
    mx = int(math.cos(r) * ml)
    my = -int(math.sin(r) * ml)
    
    a = 90.0 - ((h + (m/60) )/ 12.0) * 360.0
    r = a * math.pi / 180.0
    hx = int(math.cos(r) * hl)
    hy = -int(math.sin(r) * hl)
 
    print(h, ":" ,m)
    draw.ellipse((ctop, ctop, cbottom, cbottom), fill = 0, outline =255)
    draw.line([center,center,center+mx,center+my], fill=255, width=0)
    draw.line([center,center,center+hx,center+hy], fill=255, width=0)


    # Draw a black filled box to clear the image.

while True:
    thetime=datetime.now()
#    if(displayIsOff):
#        if (thetime.hour<=22 and thetime.hour>=6):
#            disp.poweron()
#            disp.fill(0)
#            disp.show()
#            displayIsOff=False 
#       else:
#          if (thetime.hour>23 or thetime.hour<6):
#            disp.poweroff()
#            displayIsOff=True


    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #cmd = "hostname -I | cut -d' ' -f1"
    #IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = "date +%X\ %d%b%y"
    #TimeDate = subprocess.check_output(cmd, shell=True).decode("utf-8")
    #cmd = "fetchtemp.py"
    #LocalTemp = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'gathertemps.py'
    PromData = subprocess.check_output(cmd, shell=True).decode("utf-8")
    temps=PromData.split()
    # Write four lines of text.
    draw_clock(thetime)
    draw.text((x+50, top + 0), temps[0], font=font, fill=255)
    draw.text((x+50, top + 8), temps[1], font=font, fill=255)
    draw.text((x+50, top + 16),temps[2], font=font, fill=255)
    draw.text((x+50, top + 25),temps[3], font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()
    time.sleep(0.1)

    #draw.rectangle((0, 0, width, height), outline=0, fill=0)
    #disp.poweroff()
 
#  except KeyboardInterrupt:
#    draw.rectangle((0, 0, width, height), outline=0, fill=0)
#    disp.poweroff()
#    exit()
