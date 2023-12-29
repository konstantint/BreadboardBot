from adafruit_httpserver import Server
from adafruit_motor import servo
import board
import busio
from digitalio import DigitalInOut, Direction
import espcamera
import pwmio
import socketpool
import time
import wifi


class Robot:
    """The ESP32S3 CircuitPython platform,
    Installed as described https://wiki.seeedstudio.com/XIAO_ESP32S3_CircuitPython/
    (except the image should be ESP32-S3-DevKit-C1-N8R8 to support the camera)
    """

    def __init__(self, i2c=False, uart=False, server=False, camera=False, motor_right_pin=board.IO43):
        self.led = DigitalInOut(board.IO21)
        self.led.direction = Direction.OUTPUT
        self.motor_left = servo.ContinuousServo(pwmio.PWMOut(board.IO1, frequency=50))
        self.motor_right = servo.ContinuousServo(pwmio.PWMOut(motor_right_pin, frequency=50))
        if uart:
            self.uart = busio.UART(board.IO43, board.IO44, baudrate=9600, timeout=0.1)
        if i2c:
            # Enabling I2C seems to conflict with serial debugging
            self.i2c = busio.I2C(scl=board.IO6, sda=board.IO5)
        if camera:
            self.cam_i2c = busio.I2C(scl=board.IO39, sda=board.IO40)
            self.cam = espcamera.Camera(
                data_pins=[board.IO15, board.IO17, board.IO18, board.IO16, board.IO14, board.IO12, board.IO11, board.IO48],
                pixel_clock_pin=board.IO13,
                vsync_pin=board.IO38,
                href_pin=board.IO47,
                i2c=self.cam_i2c,
                external_clock_pin=board.IO10,
                external_clock_frequency=20_000_000,
                #pixel_format=espcamera.PixelFormat.RGB565,
                pixel_format=espcamera.PixelFormat.JPEG,
                frame_size=espcamera.FrameSize.QVGA,
                framebuffer_count=2
            )
        if server:
            pool = socketpool.SocketPool(wifi.radio)
            self.server = Server(pool, "/www", debug=False)
            print(f"Starting server: {wifi.radio.ipv4_address}")
            self.server.start(str(wifi.radio.ipv4_address))

        self.led_off_time = None
        self.now = time.monotonic()

        # Welcome triple-blink / beep
        for i in range(3):
            self.blink()
            self.sleep(0.01)

    def update(self):
        self.now = time.monotonic()
        if self.led_off_time and self.now >= self.led_off_time:
            self.led.value = True
            self.led_off_time = None

    def blink(self):
        self.led.value = True
        self.led_off_time = self.now + 0.05

    def sleep(self, duration):
        now = self.now
        while self.now < now + duration:
            self.update()

    def drive(self, left_throttle, right_throttle):
        self.motor_left.throttle = 0.13 * left_throttle - 0.07
        self.motor_right.throttle = -0.11 * right_throttle

    def loop_forever(self, behaviors):
        while True:
            self.update()
            for b in behaviors:
                b(self)