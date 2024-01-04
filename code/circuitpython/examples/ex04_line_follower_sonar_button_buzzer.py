# Line-follower that will turn away from obstacles,
# report distance via beeps and play a melody on button click

from breadboardbot.platform_rp2040 import *
from breadboardbot.behaviors import *
from breadboardbot import melodies

bot = Robot(sonar=True, buzzer=True)


def stop_and_play(robot):
    robot.drive(0, 0)
    robot.play_melody(melodies.RONDO_ALLA_TURCA)


bot.loop_forever(
    behaviors=[
        RainbowAnimation(),
        ObstacleAvoidance(),
        DistanceBeeping(),
        LineFollowing(),
        OnButtonClick(stop_and_play),
    ]
)
