import board
from digitalio import DigitalInOut, Direction, Pull
import time

led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT
led.value = False  # LED on

while True:
    time.sleep(0.5)
