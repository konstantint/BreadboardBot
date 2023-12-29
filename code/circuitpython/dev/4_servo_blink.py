from adafruit_motor import servo
import board
from digitalio import DigitalInOut, Direction, Pull
import pwmio
import time

line_left = DigitalInOut(board.D10)
line_right = DigitalInOut(board.D7)

servo_left = servo.ContinuousServo(pwmio.PWMOut(board.D0, frequency=50))
servo_right = servo.ContinuousServo(pwmio.PWMOut(board.D6, frequency=50))

while True:
    servo_left.throttle = 0.1
    time.sleep(0.5)
    servo_left.throttle = 0
    time.sleep(2)
