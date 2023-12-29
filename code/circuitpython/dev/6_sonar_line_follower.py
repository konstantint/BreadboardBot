import adafruit_hcsr04
from adafruit_motor import servo
import board
from digitalio import DigitalInOut, Direction, Pull
import pwmio
import time

line_left = DigitalInOut(board.D10)
line_right = DigitalInOut(board.D7)

servo_left = servo.ContinuousServo(pwmio.PWMOut(board.D0, frequency=50))
servo_right = servo.ContinuousServo(pwmio.PWMOut(board.D6, frequency=50))

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D3)


def drive(left, right):
    servo_left.throttle = 0.1*left
    servo_right.throttle = -0.15*right


while True:
    try:
        d = sonar.distance
        print(d)
    except RuntimeError:
        pass  # Do not crash on errors from sonar
    
    if d < 10:
        drive(-1, 1)     # Turn left
        time.sleep(0.3)
    else:
        drive(line_left.value, line_right.value) # Drive along the line
