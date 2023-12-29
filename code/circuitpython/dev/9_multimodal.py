import adafruit_hcsr04
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_motor import servo
import board
from digitalio import DigitalInOut, Direction, Pull
import keypad
import neopixel
import pwmio
import simpleio
import time

line_left = DigitalInOut(board.D10)
line_right = DigitalInOut(board.D7)
servo_left = servo.ContinuousServo(pwmio.PWMOut(board.D0, frequency=50))
servo_right = servo.ContinuousServo(pwmio.PWMOut(board.D6, frequency=50))
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D3)
keys = keypad.Keys((board.D1,), value_when_pressed=False, pull=True)
rgb_pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)
rainbow = Rainbow(rgb_pixel, speed=0.1, period=2)


MODE_RAINBOW = 0
MODE_SENSE = 1
MODE_SOUND = 2
MODE_DRIVE = 3
MODE_MELODY = 4
NUM_MODES = 5
mode = MODE_RAINBOW

def melody(pin):
    melody = [(493.88, 1.0), (440, 1.0), (415.30, 1.0), (440, 1.0), (523.25, 2.0), (-1, 2.0), (587.33, 1.0),(523.25, 1.0),(493.88, 1.0),(523.25, 1.0),(659.25, 2.0),(-1, 2.0),(698.46, 1.0),(659.25, 1.0),(622.25, 1.0),(659.25, 1.0), (987.77, 1.0),(880.00, 1.0),(830.61, 1.0),(880.00, 1.0), (987.77, 1.0),(880.00, 1.0),(830.61, 1.0),(880.00, 1.0), (1046.50, 2.0), (-1, 2.0),]
    for note, duration in melody:
        simpleio.tone(board.D9, note, duration=0.1*duration)

def drive(left, right):
    servo_left.throttle = 0.1*left
    servo_right.throttle = -0.15*right

def beep():
    simpleio.tone(board.D9, 440, duration=0.05)

steps_since_last_beep = 0
smoothed_d = 0

while True:
    event = keys.events.get()
    if event and event.released:
        mode = (mode + 1) % NUM_MODES
        for i in range(mode + 1):
            beep()
            time.sleep(0.05)
    try:
        d = sonar.distance
    except RuntimeError:
        pass  # Do not crash on errors from sonar

    if mode != MODE_DRIVE: drive(0, 0)
    if mode != MODE_RAINBOW:
        rgb_pixel[0] = (0, 0, 0)
        rgb_pixel.write()

    if mode == MODE_SENSE:
        print(d)
        if steps_since_last_beep > d:
            beep()
            steps_since_last_beep = 0
        steps_since_last_beep += 1
    elif mode == MODE_SOUND:
        smoothed_d = 0.3*d + 0.7*smoothed_d
        if d < 100:
            simpleio.tone(board.D9, smoothed_d * 50, 0.2)
    elif mode == MODE_RAINBOW:
        rainbow.animate()
    elif mode == MODE_MELODY:
        melody(board.D9)
        mode = MODE_RAINBOW
    elif mode == MODE_DRIVE:
        if d < 10:
            drive(-1, 1)     # Turn left
            time.sleep(0.3)
        else:
            drive(line_left.value, line_right.value) # Drive along the line
