# Relay control on D0 (Extension board lower left grove port)
from adafruit_motor import servo
import board
from digitalio import DigitalInOut, Direction
import pwmio
import time

DigitalIn = DigitalInOut # For clarity, because that's the default

# Left & right line sensors. True when there's no line.
line_left = DigitalIn(board.D10)
line_right = DigitalIn(board.D7)

# Left & right servos
pwm_left = pwmio.PWMOut(board.D0, duty_cycle=2 ** 15, frequency=50)
servo_left = servo.ContinuousServo(pwm_left)
pwm_right = pwmio.PWMOut(board.D6, duty_cycle=2 ** 15, frequency=50)
servo_right = servo.ContinuousServo(pwm_right)

BASE_THROTTLE = 0.3

while True:
    # Turn off motor when the respective sensor sees a line (value = False)
    servo_left.throttle = BASE_THROTTLE if line_left.value else 0
    # The right servo is positioned in reverse
    servo_right.throttle = -BASE_THROTTLE if line_right.value else 0
    time.sleep(0.05)
