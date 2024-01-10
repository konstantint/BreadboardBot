# Sonar line-follower that displays things on the LED matrix

from breadboardbot.platform_rp2040 import *
from breadboardbot.behaviors import *
from breadboardbot.xiao_rgb_matrix import *


bot = Robot(sonar=True)

# Single matrix example
rgb_matrix = XiaoRGBMatrix(pin_right=board.D9)
# Alternatively, with two matrices:
# rgb_matrix = XiaoRGBMatrix(pin_left=board.D8, pin_right=board.D9)
scrolling_text = ScrollingText(rgb_matrix, "Hello!", rainbow=True)


bot.loop_forever(
    behaviors=[
        LineFollowing(),
        ObstacleAvoidance(),
        TimedSequence(
            [
                (scrolling_text, 6),
                (DemoAnimation(rgb_matrix), 10),
                # set_text resets the scroll to position 0
                (lambda _: scrolling_text.set_text("Hello!"), 0),
            ]
        ),
    ]
)
