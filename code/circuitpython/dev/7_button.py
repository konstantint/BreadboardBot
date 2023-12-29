import board
from digitalio import DigitalInOut, Direction, Pull

button = DigitalInOut(board.D1)
button.pull = Pull.UP

led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT

while True:
    led.value = button.value
