import time
import board
from digitalio import DigitalInOut, Direction, Pull

rgb = [DigitalInOut(board.LED_RED),
       DigitalInOut(board.LED_GREEN),
       DigitalInOut(board.LED_BLUE)]

for pin in rgb:
    pin.direction = Direction.OUTPUT
    pin.value = 1

switch = DigitalInOut(board.D1) #Expansion Board User Button
switch.direction = Direction.INPUT
switch.pull = Pull.UP

next_light = 0

while True:
    time.sleep(0.2)
    if switch.value == 0:
        for pin in rgb: pin.value = 0
    else:
        next_light += 1
        if next_light > 2: next_light = 0
        rgb[next_light].value = not rgb[next_light].value
