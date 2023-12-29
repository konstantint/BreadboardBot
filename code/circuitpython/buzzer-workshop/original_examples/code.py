import board
import simpleio
from digitalio import DigitalInOut, Direction, Pull
import time

input = DigitalInOut(board.D0)
input.direction = Direction.INPUT
input.pull = Pull.DOWN

while True:
    if input.value == False:
        simpleio.tone(board.LED_BLUE, 100, duration=0.3)
    time.sleep(0.1)
