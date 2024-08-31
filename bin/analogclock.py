import time
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import math

import digitalio
import board

from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display import st7789

# Configuration for CS and DC pins for Raspberry Pi
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
BAUDRATE = 64000000  # The pi can be very fast!
# Create the ST7789 display:
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=240,
    height=240,
    x_offset=0,
    y_offset=80,
    rotation=270
)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


width = display.width
height = display.height
#width = 250
#height = 250
image = Image.new("RGB", (width, height))
rotation = 180
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# Define some constants to allow easy resizing of shapes.
padding = +4
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


while True:
    try:
        thetime=datetime.now()
        draw_clock(thetime)
        display.image(image)
        #display.show()
        time.sleep(0.1)


    
    except Exception as e:
        print(e)
