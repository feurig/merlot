import time
#import subprocess
#from board import SCL, SDA, D4
#import busio
#import digitalio
from PIL import Image, ImageDraw, ImageFont
# import adafruit_ssd1305
from datetime import datetime
import math

# width = disp.width
# height = disp.height
width = 250
height = 250
image = Image.new("1", (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Define some constants to allow easy resizing of shapes.
padding = +2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

def draw_clock(t: datetime):
    center=(bottom-top)/2

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
    draw.ellipse((top, top, bottom, bottom), fill = 0, outline =255)
    draw.line([center,center,center+mx,center+my], fill=255, width=0)
    draw.line([center,center,center+hx,center+hy], fill=255, width=0)

onlyonce = True
while onlyonce:
    thetime=datetime.now()
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw_clock(thetime)
    # Display image.
    #disp.image(image)
    image.show()
    time.sleep(0.1)
    onlyonce = False


