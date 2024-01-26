# A BreadboardBot example that uses DC motors with an H-Bridge (DRV8833, or L298N) driver.

from adafruit_led_animation.animation.rainbow import Rainbow
import adafruit_mpu6050
import board
from breadboardbot import motors
from digitalio import DigitalInOut, Direction
import math
import neopixel
import time


class Robot:
    def __init__(
        self,
        line_sensors=True,
        i2c=False,
        mpu=False,
        # Use board.D6 for the DRV8833 example, board.D5 for the Mini L298N
        line_left_pin=board.D5
    ):
        self.led = DigitalInOut(board.LED_GREEN)
        self.led.direction = Direction.OUTPUT
        self.led_blue = DigitalInOut(board.LED_BLUE)
        self.led_blue.direction = Direction.OUTPUT
        self.led_blue.value = True
        self.led_red = DigitalInOut(board.LED_RED)
        self.led_red.direction = Direction.OUTPUT
        self.led_red.value = True
        self.motors = motors.HBridgeDCMotors(board.D9, board.D10, board.D7, board.D8)
        if line_sensors:
            self.line_left = DigitalInOut(line_left_pin)
            self.line_right = DigitalInOut(board.D0)
        if i2c or mpu:
            self.i2c = board.I2C()
        if mpu:
            self.mpu = adafruit_mpu6050.MPU6050(self.i2c)
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
        self.led.value = False
        self.led_off_time = self.now + 0.05

    def sleep(self, duration):
        now = self.now
        while self.now < now + duration:
            self.update()

    def get_balance_angle(self):
        """Returns a "balancing" angle in degrees by reading the MPU.

        Returns value around -180 = Face up, -90 = Straight, 0 = Face down.
        """
        # Z axis points back, X points up
        acc_x, acc_y, acc_z = self.mpu.acceleration
        return math.atan2(acc_x, -acc_z)*180/math.pi
    
    def loop_forever(self, behaviors):
        while True:
            self.update()
            for b in behaviors:
                b(self)
