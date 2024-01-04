# Sonar line-follower that displays things on the LED matrix

from breadboardbot.platform_rp2040 import *
from breadboardbot.behaviors import *
from breadboardbot.xiao_rgb_matrix import *


bot = Robot(sonar=True)
rgb_matrix = XiaoRGBMatrix(board.D9)
scrolling_text = ScrollingText(rgb_matrix, "Hello")

bot.loop_forever(
    behaviors=[
        LineFollowing(),
        ObstacleAvoidance(),
        TimedSequence(
            [
                (scrolling_text, 3),
                (lambda _: rgb_matrix.demo_animation.animate(), 20),
                # set_text resets the scroll to position 0
                (lambda _: scrolling_text.set_text("Hello"), 0),
            ]
        ),
    ]
)
