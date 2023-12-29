import time
import displayio
import terminalio
import busio
import board
import adafruit_displayio_ssd1306
import adafruit_pcf8563

from adafruit_display_text import label

displayio.release_displays()

i2c = busio.I2C(scl=board.SCL, sda=board.SDA)

font = terminalio.FONT

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)  # The address of my Board
rtc = adafruit_pcf8563.PCF8563(i2c)

oled = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

if False:  # change to False if you don't want to set the time!
    #                     year, mon, date, hour, min, sec, wday, yday, isdst
    t = time.struct_time((2022, 11, 17, 22, 44, 0, 0, -1, -1))
    # you must set year, mon, date, hour, min, sec and weekday
    # yearday is not supported, isdst can be set but we don't do anything with it at this time
    print("Setting time to:", t)  # uncomment for debugging
    rtc.datetime = t

while True:
    current = rtc.datetime

    time_display = "{:d}:{:02d}:{:02d}".format(current.tm_hour, current.tm_min, current.tm_sec)
    date_display = "{:d}/{:d}/{:d}".format(current.tm_mday, current.tm_mon, current.tm_year)
    text_display = "CircuitPython Time"

    clock = label.Label(font, text=time_display)
    date = label.Label(font, text=date_display)
    text = label.Label(font, text=text_display)

    (_, _, width, _) = clock.bounding_box
    clock.x = oled.width // 2 - width // 2
    clock.y = 5

    (_, _, width, _) = date.bounding_box
    date.x = oled.width // 2 - width // 2
    date.y = 15

    (_, _, width, _) = text.bounding_box
    text.x = oled.width // 2 - width // 2
    text.y = 25

    watch_group = displayio.Group()
    watch_group.append(clock)
    watch_group.append(date)
    watch_group.append(text)

    oled.show(watch_group)
