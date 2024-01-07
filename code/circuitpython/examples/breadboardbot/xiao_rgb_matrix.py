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
    def __init__(self, pin, left_orientation=True):
        # left_orientation = True for a matrix with its 5V & IN pins near the left robot wheel
        # left_orientation = False for a matrix with its 5V & IN pins oriented towards the right robot wheel
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
            # Height & width are flipped here because of rotation=3 or 1
            self.height,
            self.width,
            alternating=False,
        )
        self.framebuf.rotation = 3 if left_orientation else 1
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


RAINBOW = [0xFF0000, 0xFFA500, 0xFFFF00, 0x008000, 0x0000FF, 0x4B0082, 0xEE82EE]


class ScrollingText:
    """Scrolls text over one or more RGB matrices, positioned left to right."""

    def __init__(
        self,
        rgb_matrices,
        text,
        text_color=0x444444,
        background_color=0x000000,
        shift_delay=0.1,
        repeat=True,
        rainbow=False,  # When True, text_color is ignored
    ):
        self._rgb_matrices = rgb_matrices
        self._total_width = sum(m.width for m in self._rgb_matrices)
        self._text_color = text_color
        self._background_color = background_color
        self._shift_delay = shift_delay
        self._rainbow = rainbow
        self._repeat = repeat
        self.set_text(text)

    def set_text(self, value):
        self._text = value
        # Pad the text with screen width from both sides to allow it to
        # scroll into and out of the screen
        self._text_width_pixels = len(value) * 4 + 2 * self._total_width
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
        accumulated_shift = shift
        for m in self._rgb_matrices:
            self._show_text(m, accumulated_shift)
            accumulated_shift += m.width

    def _show_text(self, matrix, shift):
        matrix.framebuf.fill(self._background_color)
        if self._rainbow:
            col_id = 0
            pos = self._total_width - shift
            for char in self._text:
                matrix.framebuf.text(
                    char,
                    pos,
                    0,
                    RAINBOW[col_id % len(RAINBOW)],
                    font_name="fonts/tom_thumb.bin",
                )
                pos += 4
                col_id += 1
        else:
            matrix.framebuf.text(
                self._text,
                self._total_width - shift,
                0,
                self._text_color,
                font_name="fonts/tom_thumb.bin",
            )
        matrix.framebuf.display()
