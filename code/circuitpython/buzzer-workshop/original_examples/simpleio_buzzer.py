# See https://learn.adafruit.com/using-piezo-buzzers-with-circuitpython-arduino/circuitpython
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-neopixel
import board
import time
import simpleio
import neopixel
from analogio import AnalogIn

i = 100
while True:
    i += 10
    simpleio.tone(board.D5, i, duration=0.1)
    print("Hi")
    if i > 200:
        i = 100
