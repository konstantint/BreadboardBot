from adafruit_display_text import label
import adafruit_displayio_ssd1306
from adafruit_motor import servo
import adafruit_mpu6050
import board
from digitalio import DigitalInOut, Direction, Pull
import displayio
import pwmio
import random
import terminalio
import time

displayio.release_displays()
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)
mpu = adafruit_mpu6050.MPU6050(i2c)

servo_left = servo.ContinuousServo(pwmio.PWMOut(board.D0, frequency=50))
servo_right = servo.ContinuousServo(pwmio.PWMOut(board.D6, frequency=50))

acc_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=0, y=15, scale=1)
gyr_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=0, y=30, scale=1)
err_label = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=0, y=45, scale=1)
page = displayio.Group()
page.append(acc_label)
page.append(gyr_label)
page.append(err_label)

display.show(page)

Kp = 0.2

while True:
    acc = mpu.acceleration
    acc_label.text = "A:% .2f % .2f % .2f" % acc # m/s^2
    gyr_label.text = "G:% .2f % .2f % .2f" % mpu.gyro   # rad/s


    if acc[0] < 10.3:
        error = max(min(acc[2]*0.1, 1.0), -1.0)
    else:
        error = 0.0
    err_label.text = str(error)

    servo_left.throttle = Kp*error
    servo_right.throttle = -Kp*error*(1.5 if error > 0 else 1.0)
    time.sleep(0.01)
