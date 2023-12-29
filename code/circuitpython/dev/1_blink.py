import board
from digitalio import DigitalInOut, Direction, Pull
import time

led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT

while True:
    led.value = False   # LED on
    time.sleep(0.5)
    led.value = True    # LED off
    time.sleep(0.5)
