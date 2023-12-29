from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_motor import servo
from analogio import AnalogIn
import board
from digitalio import DigitalInOut, Direction, Pull
import keypad
import neopixel
import pwmio
import random
import time


dx = AnalogIn(board.A2)
dy = AnalogIn(board.A3)
keys = keypad.Keys((board.D4,), value_when_pressed=False, pull=True)

servo_left = servo.ContinuousServo(pwmio.PWMOut(board.D0, frequency=50))
servo_right = servo.ContinuousServo(pwmio.PWMOut(board.D6, frequency=50))

rgb_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
rainbow = Rainbow(rgb_pixel, speed=0.1, period=2)

def get_joystick(pin):
    # Y is 1.0 .. -1.0 (left-right)
    # X is -1.0.. 1.0 (front-back)
    return (pin.value * 2) / 65536 - 1.0

rainbow_on = False
while True:
    event = keys.events.get()
    if event and event.released:
        rainbow_on = not rainbow_onbb
        if not rainbow_on:
            rgb_pixel[0] = (0, 0, 0)
            rgb_pixel.write()
    if rainbow_on:
        rainbow.animate()
    throttle = get_joystick(dx)
    turn = get_joystick(dy)
    servo_left.throttle = -(throttle + turn) / 2 * 0.3
    servo_right.throttle = (throttle - turn) / 2 * 0.3
    time.sleep(0.01)
