from adafruit_display_text import label
from adafruit_display_shapes import  circle
from adafruit_display_shapes import  line
import adafruit_displayio_ssd1306
from adafruit_motor import servo
import board
from digitalio import DigitalInOut, Direction, Pull
import displayio
import pwmio
import random
import terminalio
import time

line_left = DigitalInOut(board.D10)
line_right = DigitalInOut(board.D7)

servo_left = servo.ContinuousServo(pwmio.PWMOut(board.D0, frequency=50))
servo_right = servo.ContinuousServo(pwmio.PWMOut(board.D6, frequency=50))

displayio.release_displays()
# SDA=D4, SCL=D5
display_bus = displayio.I2CDisplay(board.I2C(), device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)


class Face(displayio.Group):
    def __init__(self):
        super().__init__()
        self.mouth_height = 5
        self.mouth_width = 40
        self.pupil_radius = 4
        self.eye_radius = 10
        self.eye_level = self.eye_radius + 4
        self.mouth_top = self.eye_level + 25
        self.eye_shift = 20
        self.pupil_shift = 0
        self.text = "Hi!"
        self._build()

    def _build(self):
        self.left_eye = circle.Circle(x0=64-self.eye_shift, y0=self.eye_level, r=self.eye_radius, fill=0, outline=0xFFFFFF)
        self.right_eye= circle.Circle(x0=64+self.eye_shift, y0=self.eye_level, r=self.eye_radius, fill=0, outline=0xFFFFFF)
        self.left_pupil = circle.Circle(x0=64-self.eye_shift + self.pupil_shift, y0=self.eye_level, r=self.pupil_radius, fill=0xFFFFFF)
        self.right_pupil = circle.Circle(x0=64+self.eye_shift + self.pupil_shift, y0=self.eye_level, r=self.pupil_radius, fill=0xFFFFFF)
        self.mouth_left = line.Line(64-self.mouth_width//2, self.mouth_top, 64, self.mouth_top + self.mouth_height, color=0xfffff)
        self.mouth_right = line.Line(64, self.mouth_top + self.mouth_height, 64+self.mouth_width//2, self.mouth_top, color=0xfffff)
        self.text_area = label.Label(terminalio.FONT, text=self.text, color=0xFFFF00, x=0, y=64-10)
        for obj in [self.left_eye, self.right_eye, self.left_pupil, self.right_pupil, self.mouth_left, self.mouth_right, self.text_area]:
            self.append(obj)

    def look(self, direction):
        self.pupil_shift = direction*(self.eye_radius - self.pupil_radius - 2)
        self.left_pupil.x0 = 64 - self.eye_shift + self.pupil_shift
        self.right_pupil.x0 = 64 + self.eye_shift + self.pupil_shift


face = Face()
display.show(face)
eye_cycle = 0

while True:
    servo_left.throttle = 0.1 * line_left.value
    servo_right.throttle = -0.15 * line_right.value
    face.look(int(line_right.value) - int(line_left.value))
