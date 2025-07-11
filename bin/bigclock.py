#!/usr/bin/python3

import time
import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
from datetime import datetime

i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_I2C(i2c, 20, 4)
lcd.backlight = True
#lcd.message = "Hello there welcom\nCircuitPython\nwho knows if \nthis is too bright"
customchars=[
    bytes([0x01, 0x07, 0x0F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F]),      # char 0: top left triangle
    bytes([0x00, 0x00, 0x00, 0x00, 0x1F, 0x1F, 0x1F, 0x1F]),      # char 1: bottom block
    bytes([0x10, 0x1C, 0x1E, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F]),      # char 2: top right triangle
    bytes([0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x0F, 0x07, 0x01]),      # char 3: bottom left triangle
    bytes([0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1E, 0x1C, 0x10]),      # char 4: bottom right triangle
    bytes([0x1F, 0x1F, 0x1F, 0x1F, 0x00, 0x00, 0x00, 0x00]),      # char 5: upper block
    bytes([0x1F, 0x1F, 0x1E, 0x1C, 0x18, 0x18, 0x10, 0x10]),      # char 6: full bottom right triangle
    bytes([0x01, 0x07, 0x0F, 0x1F, 0x00, 0x00, 0x00, 0x00])       # char 7: top left triangle
]
for ch in range(8):
    lcd.create_char(ch, customchars[ch])

mess=""
for ch in range(8):
    mess+=chr(ch)

lcd.message=mess

bn4 = [                            # 4-line numbers
#         0              1              2              3              4              5              6              7              8              9
  ["\x00\x05\x02","\x07\xFF\xFE","\x07\x05\x02","\x07\x05\x02","\xff\xFE\xff","\xff\x05\x05","\x00\x05\x02","\x05\x05\xff","\x00\x05\x02","\x00\x05\x02"],
  ["\xFF\xFE\xFF","\xFE\xFF\xFE","\xfe\x2f\x06","\xFE\x01\x04","\xff\x01\xFF","\xFf\x01\xa4","\xFF\xFE\xFE","\xFE\x2f\x06","\x03\x01\x04","\x03\x01\xff"],
  ["\xFF\xFE\xFF","\xFE\xFF\xFE","\x2F\x06\xFE","\xFE\xfe\x02","\xfe\xfe\xFF","\xfe\xfe\xff","\xFF\x05\x02","\xFE\xff\xfe","\x00\xfe\x02","\xfe\xfe\xFF"],
  ["\x03\x01\x04","\xFE\xFF\xFE","\xff\x01\x01","\x03\x01\x04","\xfe\xFE\xFF","\x03\x01\x04","\x03\x01\x04","\xfe\xff\xFe","\x03\x01\x04","\x03\x01\x04"],

]

def printNum4(digit, leftAdjust):
    for row in range(4):
        lcd.cursor_position(leftAdjust,row);
        lcd.message=bn4[row][digit]

def printShort1(clear=False ):
    for row in range(4):
        lcd.cursor_position(0,row);
        if (clear):
            lcd.message="\xfe\xfe"
        else:
            lcd.message=bn4[row][1][0:2]

def printColon(leftAdjust):
    clearCollumn(leftAdjust)
    lcd.cursor_position(leftAdjust,1)
    lcd.message="\xa5"
    lcd.cursor_position(leftAdjust,2)
    lcd.message="\xa5"

def clearCollumn(col=6):
   for row in range(4):
        lcd.cursor_position(col,row)
        lcd.message="\xfe"


def printTime():
    date_string = f'{datetime.now():%I%M%p}'
    if (date_string[0] == '1'):
        printShort1()
    else:
        printShort1(clear=True)
    clearCollumn(2)
    printNum4(int(date_string[1]),3)
    printColon(6);
    printNum4(int(date_string[2]),7)
    clearCollumn(10)
    printNum4(int(date_string[3]),11)
    lcd.cursor_position(14,0)
    lcd.message=date_string[:-2]
    lcd.cursor_position(15,1)
    lcd.message=datetime.now().strftime("%d%b")
    
if __name__ == '__main__':
    while True:
        printTime()
        time.sleep(5)
