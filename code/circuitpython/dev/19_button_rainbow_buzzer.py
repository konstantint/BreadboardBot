from adafruit_led_animation.animation.rainbow import Rainbow
import board
from digitalio import DigitalInOut, Direction, Pull
import keypad
import neopixel
import simpleio
import time

rgb_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
rainbow = Rainbow(rgb_pixel, speed=0.1, period=2)

keys = keypad.Keys((board.D8,), value_when_pressed=False, pull=True)

led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT

rainbow_on = False

melody = [(493.88, 1.0), (440, 1.0), (415.30, 1.0), (440, 1.0), (523.25, 2.0), (-1, 2.0), (587.33, 1.0),(523.25, 1.0),(493.88, 1.0),(523.25, 1.0),(659.25, 2.0),(-1, 2.0),(698.46, 1.0),(659.25, 1.0),(622.25, 1.0),(659.25, 1.0), (987.77, 1.0),(880.00, 1.0),(830.61, 1.0),(880.00, 1.0), (987.77, 1.0),(880.00, 1.0),(830.61, 1.0),(880.00, 1.0), (1046.50, 2.0), (-1, 2.0),]
def play_melody(pin):
    for note, duration in melody:
        if note >= 0:
            simpleio.tone(pin, note, duration*0.1)
        else:
            time.sleep(duration*0.1)

while True:
    event = keys.events.get()
    if event:
        if event.released:
            rainbow_on = False
            rgb_pixel[0] = (0, 0, 0)
            rgb_pixel.write()
        else:
            rainbow_on = True
            play_melody(board.D9)
    if rainbow_on:
        rainbow.animate()
