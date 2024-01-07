# Sonar line-follower that displays things on the LED matrix

from breadboardbot.platform_rp2040 import *
from breadboardbot.behaviors import *
from breadboardbot.xiao_rgb_matrix import *


bot = Robot(sonar=True)
# Single matrix example
matrices = [XiaoRGBMatrix(board.D9)]
# Alternatively, with two matrices:
# matrices = [XiaoRGBMatrix(board.D8, left_orientation=False), XiaoRGBMatrix(board.D9)]
scrolling_text = ScrollingText(matrices, "Hello!", rainbow=True)


bot.loop_forever(
    behaviors=[
        LineFollowing(),
        ObstacleAvoidance(),
        TimedSequence(
            [
                (scrolling_text, 6),
                (
                    lambda _: list(map(lambda x: x.demo_animation.animate(), matrices)),
                    20,
                ),
                # set_text resets the scroll to position 0
                (lambda _: scrolling_text.set_text("Hello!"), 0),
            ]
        ),
    ]
)
