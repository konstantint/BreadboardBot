import board
import busio
from adafruit_display_text import label
from adafruit_display_shapes import  circle
from adafruit_display_shapes import  line
import adafruit_displayio_ssd1306
from adafruit_motor import servo
import board
from digitalio import DigitalInOut, Direction, Pull
import displayio
import face
import pwmio
import random
import terminalio
import time
import hc05controller

#line_left = DigitalInOut(board.D10)
#line_right = DigitalInOut(board.D7)

servo_left = servo.ContinuousServo(pwmio.PWMOut(board.D0, frequency=50))
servo_right = servo.ContinuousServo(pwmio.PWMOut(board.D8, frequency=50))

displayio.release_displays()
# SDA=D4, SCL=D5
display_bus = displayio.I2CDisplay(board.I2C(), device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)

controller = hc05controller.HC05Controller()

face = face.Face()
display.show(face)
eye_cycle = 0

def drive(throttle, turn):
    left, right = throttle - turn, throttle + turn
    servo_left.throttle = min(1, max(-1, left))
    servo_right.throttle = min(1, max(-1, -1.1*right))

turn_rate = 0
throttle = 0
DELTA_TURN = 0.01
DELTA_THROTTLE = 0.01

left_held = right_held = fwd_held = back_held = False

while True:
    cmd = controller.read_command()
    if cmd is not None:
        if cmd == b"0":
            left_held = right_held = fwd_held = back_held = False
        elif cmd == b"L":
            left_held = True
        elif cmd == b"R":
            right_held = True
        elif cmd == b"F":
            fwd_held = True
        elif cmd == b"B":
            back_held = True
        elif cmd == b"S":
            face.look(-1)
        elif cmd == b"C":
            face.look(1)
        elif cmd == b"P":
            throttle = turn_rate = 0
        elif cmd.startswith(b"say "):
            face.say(cmd[4:].decode("ascii"))
        else:
            print(cmd)
    if left_held: turn_rate += DELTA_TURN
    if right_held: turn_rate -= DELTA_TURN
    if fwd_held: throttle += DELTA_THROTTLE
    if back_held: throttle -= DELTA_THROTTLE
    drive(throttle, turn_rate)
    #face.say(str(throttle) + " " + str(turn_rate))
    time.sleep(0.02)


