# A BreadboardBot example that uses DC motors with an H-Bridge (DRV8833, or L298N) driver.

from adafruit_led_animation.animation.rainbow import Rainbow
import board
from breadboardbot import motors
from digitalio import DigitalInOut, Direction
import neopixel
import time


class Robot:
    def __init__(
        self,
        line_sensors=True,
        # Use board.D6 for the DRV8833 example, board.D5 for the Mini L298N
        line_left_pin=board.D5
    ):
        self.led = DigitalInOut(board.LED_GREEN)
        self.led.direction = Direction.OUTPUT
        self.motors = motors.HBridgeDCMotors(board.D9, board.D10, board.D7, board.D8)
        if line_sensors:
            self.line_left = DigitalInOut(line_left_pin)
            self.line_right = DigitalInOut(board.D0)
        self.rgb_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
        self.rainbow = Rainbow(self.rgb_pixel, speed=0.1, period=2)
        self.led_off_time = None
        self.now = time.monotonic()

        # Welcome triple-blink
        for i in range(3):
            self.blink()
            self.sleep(0.1)

    def update(self):
        self.now = time.monotonic()
        if self.led_off_time and self.now >= self.led_off_time:
            self.led.value = True
            self.led_off_time = None

    def blink(self):
        self.led.value = True
        self.led_off_time = self.now + 0.05

    def sleep(self, duration):
        now = self.now
        while self.now < now + duration:
            self.update()

    def loop_forever(self, behaviors):
        while True:
            self.update()
            for b in behaviors:
                b(self)
