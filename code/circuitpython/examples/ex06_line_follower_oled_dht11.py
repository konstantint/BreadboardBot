# Line follower with a funny face that shows temperature and humidity.

from breadboardbot.behaviors import *
from breadboardbot.display import *
from breadboardbot.face import *
from breadboardbot.platform_rp2040 import *

bot = Robot(dht11=True, i2c=True)
face = Face()


def update_face(robot):
    face.look(int(robot.line_right.value) - int(robot.line_left.value))
    face.say(
        "Temp: "
        + str(robot.dht11.temperature)
        + "C  Hum: "
        + str(robot.dht11.humidity)
        + "%"
    )


bot.loop_forever(
    behaviors=[
        LineFollowing(),
        DisplayBehavior(bot.i2c, face, update_face),
    ]
)
