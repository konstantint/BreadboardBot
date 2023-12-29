from adafruit_motor.servo import ContinuousServo
import board
from digitalio import DigitalInOut, Direction
from ibusrx import IBusRx
from pwmio import PWMOut

rgb = [DigitalInOut(board.LED_RED),
       DigitalInOut(board.LED_GREEN),
       DigitalInOut(board.LED_BLUE)]
for led in rgb:
    led.direction = Direction.OUTPUT
    led.value = True

# Left & right servos
servo_left = ContinuousServo(PWMOut(board.D0, duty_cycle=2 ** 15, frequency=50))
servo_right = ContinuousServo(PWMOut(board.D6, duty_cycle=2 ** 15, frequency=50))

# Receiver
rx = IBusRx(board.RX)

def control(arm, throttle, yaw):
    if arm:
        left, right = throttle + yaw, throttle - yaw
        if left < -1.0: left = -1.0
        if left > 1.0: left = 1.0
        if right < -1.0: right = -1.0
        if right > 1.0: right = 1.0
        return left, right
    else:
        return 0.0, 0.0

def drive(left, right):
    servo_left.throttle, servo_right.throttle = -left, right

ctr = 0
while True:
    rx.loop()
    # Show red when not connected, green when connected
    rgb[0].value = rx.loops_since_valid_packet < 1000
    rgb[1].value = not rgb[0].value
    # Blue shows the arm state
    rgb[2].value = rx.channels[5] < 1500

    if rx.loops_since_valid_packet < 100:
        arm = rx.channels[5] > 1500
        throttle = (rx.channels[2] - 1000) / 1000
        yaw = (rx.channels[0] - 1500) / 500
        drive(*control(arm, throttle, yaw))
    elif rx.loops_since_valid_packet < 500:
        drive(*control(False, 0.0, 0.0))

    ctr += 1
    if ctr == 100:
        ctr = 0
