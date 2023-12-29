from adafruit_led_animation.animation.rainbow import Rainbow
import board
from digitalio import DigitalInOut, Direction, Pull
import neopixel

rgb_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
rainbow = Rainbow(rgb_pixel, speed=0.1, period=2)

button = DigitalInOut(board.D1)
button.pull = Pull.UP

led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT

while True:
    if not button.value:
        rainbow.animate()
    else:
        rgb_pixel[0] = (0, 0, 0)
        rgb_pixel.write()
