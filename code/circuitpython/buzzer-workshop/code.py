import board
import time
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT

led.value = False

while True:
    time.sleep(0.1)
