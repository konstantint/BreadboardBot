import board
from digitalio import DigitalInOut, Direction, Pull
import time

led_green = DigitalInOut(board.LED_GREEN)
led_green.direction = Direction.OUTPUT
led_red = DigitalInOut(board.LED_RED)
led_red.direction = Direction.OUTPUT

line_left = DigitalInOut(board.D10)
line_right = DigitalInOut(board.D7)

while True:
    led_green.value = line_left.value
    led_red.value = line_right.value
