# The simplest ever line-follower.

from breadboardbot.platform_rp2040 import *
from breadboardbot.behaviors import *

bot = Robot()
bot.loop_forever(behaviors=[LineFollowing()])
