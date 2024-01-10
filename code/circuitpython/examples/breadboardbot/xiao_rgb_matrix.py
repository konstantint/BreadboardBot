import adafruit_framebuf
from adafruit_led_animation.grid import PixelGrid, VERTICAL
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


class XiaoRGBMatrix(adafruit_framebuf.FrameBuffer):
    """Version of adafruit_pixel_framebuf.PixelFramebuffer for
    one or two Xiao RGB matrices attached to the BreadboardBot.

    Supports three configurations:
        - a single "right-side" matrix (attached with the 5V and IN
          pins looking towards the left robot wheel),
        - a single "left-side" matrix (attached with the 5V and IN
          pins looking towards the right robot wheel),
        - both matrices attached next to each other, forming a single
          screen.
    """

    def __init__(self, pin_left=None, pin_right=None, brightness=0.1) -> None:
        self._height = 6
        self._width = 0
        if pin_left:
            self.pixels_left = neopixel.NeoPixel(
                pin_left,
                6 * 10,
                brightness=brightness,
                auto_write=False,
            )
            self._grid_left = PixelGrid(
                self.pixels_left,
                width=10,
                height=6,
                orientation=VERTICAL,
                alternating=False,
                reverse_y=True,
            )
            self._width += 10
        else:
            self.pixels_left = None
            self._grid_left = None
        if pin_right:
            self.pixels_right = neopixel.NeoPixel(
                pin_right,
                6 * 10,
                brightness=brightness,
                auto_write=False,
            )
            self._grid_right = PixelGrid(
                self.pixels_right,
                width=10,
                height=6,
                orientation=VERTICAL,
                alternating=False,
                reverse_x=True,
            )
            self._width += 10
        else:
            self.pixels_right = None
            self._grid_right = None

        self._buffer = bytearray(self._width * self._height * 3)
        self._double_buffer = bytearray(self._width * self._height * 3)
        super().__init__(
            self._buffer, self._width, self._height, buf_format=adafruit_framebuf.RGB888
        )

    def display(self) -> None:
        """Copy the raw buffer changes to one or two grids and show"""
        x_offset = 0
        if self._grid_left:
            for _x in range(10):
                for _y in range(self._height):
                    index = (_y * self.stride + _x) * 3
                    if (
                        self._buffer[index : index + 3]
                        != self._double_buffer[index : index + 3]
                    ):
                        self._grid_left[(_x, _y)] = tuple(
                            self._buffer[index : index + 3]
                        )
                        self._double_buffer[index : index + 3] = self._buffer[
                            index : index + 3
                        ]
            x_offset += 10
            self._grid_left.show()
        if self._grid_right:
            for _x in range(10):
                for _y in range(self._height):
                    index = (_y * self.stride + _x + x_offset) * 3
                    if (
                        self._buffer[index : index + 3]
                        != self._double_buffer[index : index + 3]
                    ):
                        self._grid_right[(_x, _y)] = tuple(
                            self._buffer[index : index + 3]
                        )
                        self._double_buffer[index : index + 3] = self._buffer[
                            index : index + 3
                        ]
            self._grid_right.show()


class DemoAnimation:
    """A demo animation behavior on one or two Xiao RGB matrices."""

    def __init__(self, rgb_matrix):
        self._rgb_matrix = rgb_matrix
        self.pixels = []
        if rgb_matrix.pixels_left:
            self.pixels.append(rgb_matrix.pixels_left)
        if rgb_matrix.pixels_right:
            self.pixels.append(rgb_matrix.pixels_right)
        self.animations = []
        for p in self.pixels:
            self.animations.append(
                AnimationSequence(
                    # Blink(p, speed=0.5, color=JADE)
                    # ColorCycle(p, speed=0.4, colors=[MAGENTA, ORANGE])
                    # Comet(p, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
                    # Chase(p, speed=0.1, size=3, spacing=6, color=WHITE)
                    RainbowComet(p, speed=0.03, tail_length=7, bounce=True),
                    RainbowSparkle(p, speed=0.1, num_sparkles=15),
                    # Rainbow(p, speed=0.1, period=2),
                    RainbowChase(p, speed=0.1, size=3, spacing=2, step=8),
                    Pulse(p, speed=0.02, period=3, color=AMBER),
                    # Sparkle(p, speed=0.1, color=PURPLE, num_sparkles=10),
                    # Solid(p, color=JADE)
                    # SparklePulse(p, speed=0.1, period=3, color=JADE)
                    # CustomColorChase(
                    #     p, speed=0.1, size=2, spacing=3, colors=[ORANGE, WHITE, JADE]
                    # ),
                    advance_interval=7,
                    auto_clear=True,
                )
            )

    def __call__(self, robot):
        for a in self.animations:
            a.animate()


RAINBOW = [0xFF0000, 0xFFA500, 0xFFFF00, 0x008000, 0x0000FF, 0x4B0082, 0xEE82EE]


class ScrollingText:
    """Scrolls text over a given pixel framebuffer."""

    def __init__(
        self,
        framebuffer,
        text,
        text_color=0x444444,
        background_color=0x000000,
        shift_delay=0.1,
        repeat=True,
        rainbow=False,  # When True, text_color is ignored
    ):
        self._framebuffer = framebuffer
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
        self._text_width_pixels = len(value) * 4 + 2 * self._framebuffer.width
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
        self._framebuffer.fill(self._background_color)
        if self._rainbow:
            col_id = 0
            pos = self._framebuffer.width - shift
            for char in self._text:
                self._framebuffer.text(
                    char,
                    pos,
                    0,
                    RAINBOW[col_id % len(RAINBOW)],
                    font_name="fonts/tom_thumb.bin",
                )
                pos += 4
                col_id += 1
        else:
            self._framebuffer.text(
                self._text,
                self._framebuffer.width - shift,
                0,
                self._text_color,
                font_name="fonts/tom_thumb.bin",
            )
        self._framebuffer.display()
