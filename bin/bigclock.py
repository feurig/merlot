!#/usr/bin/python3

#//3x2 https://exploreembedded.com/wiki/Distance_Meter_with_Big_Fonts
#const uint8_t bigNumbers3x2CustomPatterns_3[8][8] PROGMEM = {
#{ B11100, B11110, B11110, B11110, B11110, B11110, B11110, B11100}, // 0 left bar
#{ B00111, B01111, B01111, B01111, B01111, B01111, B01111, B00111}, // 1 right bar
#{ B11111, B11111, B00000, B00000, B00000, B00000, B11111, B11111}, // 2 upper and lower bar
#{ B11110, B11100, B00000, B00000, B00000, B00000, B11000, B11100}, // 3 left upper and lower rounded
#{ B01111, B00111, B00000, B00000, B00000, B00000, B00011, B00111}, // 4 right upper and lower rounded
#{ B00000, B00000, B00000, B00000, B00000, B00000, B11111, B11111}, // 5 right lower
#{ B00000, B00000, B00000, B00000, B00000, B00000, B00111, B01111}, // 6 right lower rounded
#{ B11111, B11111, B00000, B00000, B00000, B00000, B00000, B00000}  // 7 upper bar
#};

import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_I2C(i2c, 20, 4)
lcd.backlight = True
lcd.message = "Hello there welcom\nCircuitPython\nwho knows if \nthis is too bright"