#!/usr/bin/python3 
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for 16x2 character lcd connected to an MCP23008 I2C LCD backpack."""
import time
import board
import adafruit_character_lcd.character_lcd_i2c as character_lcd
import subprocess

cmd = "hostname -I | cut -d' ' -f1"
IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = "date +%X\ %d%b%y"
TimeDate = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = "fetchtemp.py"
LocalTemp = subprocess.check_output(cmd, shell=True).decode("utf-8")
cmd = 'gathertemps.py'
PromData = subprocess.check_output(cmd, shell=True).decode("utf-8")
temps=PromData.split()

# Modify this if you have a different sized Character LCD
lcd_columns = 20
lcd_rows = 4

# Initialise I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Initialise the lcd class
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)

# Turn backlight on
lcd.backlight = True
# Print a two line message
lcd.message = CMD + IP
# Wait 5s
time.sleep(5)
lcd.clear()
# Print two line message right to left
lcd.text_direction = lcd.RIGHT_TO_LEFT
lcd.message = TimeDate
# Wait 5s
time.sleep(5)
lcd.clear()
lcd.cursor = True
lcd.message = temps
# Wait 5s
time.sleep(5)
# Display blinking cursor
lcd.clear()
lcd.blink = True
lcd.message = PromData
# Wait 5s
time.sleep(5)
lcd.blink = False
lcd.clear()
lcd.clear()
lcd.message = "Going to sleep\nCya later!"
time.sleep(5)
# Turn backlight off
lcd.backlight = False
time.sleep(2)
