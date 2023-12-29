# Line-follower that will turn away from obstacles.

from breadboardbot.platform_rp2040 import *
from breadboardbot.behaviors import *

bot = Robot(sonar=True)
bot.loop_forever(behaviors=[LineFollowing(), ObstacleAvoidance()])
