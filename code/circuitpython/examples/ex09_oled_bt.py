# Robot control via Bluetooth Serial (HC05/06)

import board
from breadboardbot.display import *
from breadboardbot.face import *
from breadboardbot.hc06_controller import *
from breadboardbot.platform_rp2040 import *

bot = Robot(i2c=True, uart=True, line_sensors=False, motor_right_pin=board.D8)
face = Face()


def handle_command(cmd):
    global face, bot
    if cmd == b"S":
        face.look(-1)
    elif cmd == b"C":
        face.look(1)
    elif cmd == b"T":
        face.look(0)
    elif cmd == b"F":
        bot.motors.drive(1, 1)
    elif cmd == b"B":
        bot.motors.drive(-1, -1)
    elif cmd == b"L":
        bot.motors.drive(-1, 1)
    elif cmd == b"R":
        bot.motors.drive(1, -1)
    else:
        bot.motors.drive(0, 0)


bot.loop_forever(
    behaviors=[
        DisplayBehavior(bot.i2c, face),
        HC06Listener(bot.uart, handle_command),
    ]
)
