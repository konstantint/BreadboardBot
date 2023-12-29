import board
from digitalio import DigitalInOut, Direction, Pull
import time

led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT
line_left = DigitalInOut(board.D10)

while True:
    led.value = line_left.value
