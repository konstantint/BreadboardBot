# Xiao LED matrix behaviors
from adafruit_pixel_framebuf import PixelFramebuffer
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.sparklepulse import SparklePulse
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.customcolorchase import CustomColorChase
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import PURPLE, WHITE, AMBER, JADE, MAGENTA, ORANGE
import neopixel
import time


class XiaoRGBMatrix:
    def __init__(self, pin):
        self.pin = pin
        self.height = 6
        self.width = 10
        self.pixels = neopixel.NeoPixel(
            pin,
            self.height * self.width,
            brightness=0.1,
            auto_write=False,
        )
        self.framebuf = PixelFramebuffer(
            self.pixels,
            # Height & width are flipped here because of rotation=3
            self.height,
            self.width,
            alternating=False,
        )
        self.framebuf.rotation = 3
        self.demo_animation = AnimationSequence(
            # Blink(self.pixels, speed=0.5, color=JADE)
            # ColorCycle(self.pixels, speed=0.4, colors=[MAGENTA, ORANGE])
            # Comet(self.pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
            # Chase(self.pixels, speed=0.1, size=3, spacing=6, color=WHITE)
            RainbowComet(self.pixels, speed=0.03, tail_length=7, bounce=True),
            RainbowSparkle(self.pixels, speed=0.1, num_sparkles=15),
            # Rainbow(self.pixels, speed=0.1, period=2),
            RainbowChase(self.pixels, speed=0.1, size=3, spacing=2, step=8),
            Pulse(self.pixels, speed=0.02, period=3, color=AMBER),
            # Sparkle(self.pixels, speed=0.1, color=PURPLE, num_sparkles=10),
            # Solid(self.pixels, color=JADE)
            # SparklePulse(self.pixels, speed=0.1, period=3, color=JADE)
            # CustomColorChase(
            #     self.pixels, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
            # ),
            advance_interval=7,
            auto_clear=True,
        )


class ScrollingText:
    def __init__(
        self,
        rgb_matrix,
        text,
        text_color=0x444444,
        background_color=0x000000,
        shift_delay=0.1,
        repeat=True,
    ):
        self._rgb_matrix = rgb_matrix
        self._text_color = text_color
        self._background_color = background_color
        self._shift_delay = 0.1
        self._repeat = repeat
        self.set_text(text)

    def set_text(self, value):
        self._text = value
        self._text_width_pixels = len(value) * 4 + 2 * self._rgb_matrix.width
        self._shift_pos = 0
        self._animation_start = time.monotonic()
        self._last_shift = -1

    def __call__(self, robot):
        shift = int((robot.now - self._animation_start) / self._shift_delay)
        if self._repeat:
            shift = shift % self._text_width_pixels
        if shift == self._last_shift:
            return
        self._last_shift = shift
        self._rgb_matrix.framebuf.fill(self._background_color)
        self._rgb_matrix.framebuf.text(
            self._text,
            self._rgb_matrix.width - shift,
            0,
            self._text_color,
            font_name="fonts/tom_thumb.bin",
        )
        self._rgb_matrix.framebuf.display()
