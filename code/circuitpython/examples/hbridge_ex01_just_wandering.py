# Robot that has no sensors and just wanders around, showing off
# its RGB led.

from breadboardbot.platform_rp2040_hbridge import *
from breadboardbot.behaviors import *

bot = Robot()
bot.loop_forever(
    behaviors=[
        RainbowAnimation(),
        TimedSequence(
            [
                (lambda robot: robot.motors.drive(1, 1), 2.0),
                (lambda robot: robot.motors.drive(0, 0), 0.5),
                (lambda robot: robot.motors.drive(-1, 1), 1.0),
                (lambda robot: robot.motors.drive(0, 0), 0.5),
                (lambda robot: robot.motors.drive(1, 1), 2.0),
                (lambda robot: robot.motors.drive(0, 0), 0.5),
                (lambda robot: robot.motors.drive(1, -1), 1.0),
                (lambda robot: robot.motors.drive(0, 0), 0.5),
            ]
        ),
    ]
)
