# Relay control on D0 (Extension board lower left grove port)
import board
import time
from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False


button = DigitalInOut(board.D1) # On board button
button.direction = Direction.INPUT
button.pull = Pull.UP

relay = DigitalInOut(board.D0) # On board button
relay.direction = Direction.OUTPUT
relay.value = False

while True:
    relay.value = not button.value
    led.value = button.value
    time.sleep(0.05)