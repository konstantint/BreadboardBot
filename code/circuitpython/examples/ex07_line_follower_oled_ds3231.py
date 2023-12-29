# Line follower that somewhy shows current time and date

import adafruit_ds3231
from adafruit_display_text import label
from breadboardbot.behaviors import *
from breadboardbot.display import *
from breadboardbot.platform_rp2040 import *
import terminalio

bot = Robot(i2c=True)


class DS3231Behavior:
    def __init__(self, i2c, update_fn, initial_time=None):
        self.rtc = adafruit_ds3231.DS3231(i2c)
        if initial_time:
            self.rtc.datetime = initial_time
        self.update_fn = update_fn

    def __call__(self, robot):
        self.update_fn(self.rtc.datetime)


time_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=15, y=15, scale=2)
date_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=30, y=40, scale=1)
page = displayio.Group()
page.append(time_label)
page.append(date_label)


def update_time(dt):
    time_label.text = f"{dt.tm_hour:02}:{dt.tm_min:02}:{dt.tm_sec:02}"
    date_label.text = f"{dt.tm_mday:02}.{dt.tm_mon:02}.{dt.tm_year}"


INITIAL_TIME = None
# Once set, the DS3231 should preserve correct time between poweroffs
# (if it has a battery)
INITIAL_TIME = time.struct_time((2023, 11, 26, 17, 48, 0, -1, -1, -1))

bot.loop_forever(
    behaviors=[
        LineFollowing(),
        DisplayBehavior(bot.i2c, page),
        DS3231Behavior(bot.i2c, update_time, INITIAL_TIME),
    ]
)
