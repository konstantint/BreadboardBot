"""
Description: 
    Control rgb light with joystick (for more info see: https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel)
Cable Connections: 
    Button + -> 3V3
    Button - -> GND
    Button S -> D0
    Joystick +5W -> 3V3
    Joystick GND -> GND
    Joystick VRx -> A1
    Joystick VRy -> A2
"""
import board
import time
import simpleio
import neopixel
from analogio import AnalogIn

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
analogin1 = AnalogIn(board.A1)
analogin2 = AnalogIn(board.A2)

# Reads the value of the given pin and returns a value between 0 and 255
def get_voltage(pin):
    return (pin.value * 255) / 65536

while True:
    # Reads from the pin and sets the LED color based on the reading
    red = get_voltage(analogin1)
    green = get_voltage(analogin2)
    pixel.fill((red, green, 0))