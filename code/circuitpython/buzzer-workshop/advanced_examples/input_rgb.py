"""
Description: 
    Control rgb light with button
Cable Connections: 
    Button + -> 3V3
    Button - -> GND
    Button S -> D0
"""
import board
import simpleio
import time
import neopixel
from digitalio import DigitalInOut, Direction

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
input = DigitalInOut(board.D0)
input.direction = Direction.INPUT

# use values between 0-255
colors = [(255, 0 , 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211),]
currentColor = 0 % len(colors)

#change for other sensors
activeState = False

while True:
    
    if input.value == activeState:

        pixel.fill(colors[currentColor])
        currentColor = (currentColor + 1) % len(colors)
        time.sleep(0.5)

