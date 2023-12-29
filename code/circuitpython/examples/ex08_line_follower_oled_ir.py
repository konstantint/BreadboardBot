# Line follower with a funny face that uses an IR proximity sensor
# to avoid obstacles.

import board
from breadboardbot.behaviors import *
from breadboardbot.display import *
from breadboardbot.face import *
from breadboardbot.platform_rp2040 import *

bot = Robot(i2c=True)
face = Face()


def update_face(robot):
    face.look(int(robot.line_right.value) - int(robot.line_left.value))


bot.loop_forever(
    behaviors=[
        LineFollowing(),
        DisplayBehavior(bot.i2c, face, update_face),
        IRObstacleAvoidance(board.D8),
    ]
)
