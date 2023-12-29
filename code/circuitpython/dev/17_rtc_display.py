from adafruit_display_text import label
import adafruit_displayio_ssd1306
import adafruit_ds3231
import board
from digitalio import DigitalInOut, Direction, Pull
import displayio
import random
import terminalio
import time

displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)
rtc = adafruit_ds3231.DS3231(i2c)

time_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=15, y=15, scale=2)
date_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=30, y=40, scale=1)
page = displayio.Group()
page.append(time_label)
page.append(date_label)

SET_TIME = None
#SET_TIME = time.struct_time((2023,12,16,17,48,0,-1,-1,-1))
if SET_TIME:
    rtc.datetime = SET_TIME

display.show(page)

while True:
    t = rtc.datetime
    time_label.text = f"{t.tm_hour:02}:{t.tm_min:02}:{t.tm_sec:02}"
    date_label.text = f"{t.tm_mday:02}.{t.tm_mon:02}.{t.tm_year}"
    time.sleep(1)
