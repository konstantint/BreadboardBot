"""CircuitPython I2C Device Address Scan"""
# If you run this and it seems to hang, try manually unlocking
# your I2C bus from the REPL with
#  >>> import board
#  >>> board.I2C().unlock()

import time
import board
import displayio
import terminalio
displayio.release_displays()

import adafruit_displayio_ssd1306
from adafruit_display_text import label
from adafruit_display_shapes import  rect
import  time

# Devices
i2c = board.I2C()
display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

ch_width = (128-3)//8
channels = [
    rect.Rect(x=2 + i*ch_width, y=2, width=ch_width, height=0, fill=0xffffff) for i in range(8)
]

channels2 = [
    rect.Rect(x=2 + i*ch_width, y=2 + (64-4)//2, width=ch_width, height=0, fill=0xffffff) for i in range(8)
]

#text_area = label.Label(terminalio.FONT, text="", color=0xFFFF00, x=15, y=15)
def make_page():
    page = displayio.Group() # no max_size needed
    color_bitmap = displayio.Bitmap(128, 64, 1) # Full screen white
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    page.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(128-2, 64-2, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=1, y=1)
    page.append(inner_sprite)

    for ch in channels:
        page.append(ch)
    for ch in channels2:
        page.append(ch)
    return  page

page = make_page()
display.show(page)

M5STACK_8ANGLE_ADDR = 0x43
M5STACK_8ENCODER_ADDR = 0x41

class I2CDevice:
    def __init__(self, addr):
        self.addr = addr
    def read(self, reg, size=1):
        result = bytearray(size)
        i2c.writeto(self.addr, bytes([reg]))
        i2c.readfrom_into(self.addr, result)
        return bytes(result)
    def write(self, reg, buffer):
        i2c.writeto(self.addr, bytes([reg]) + bytes(buffer))

encoder = I2CDevice(M5STACK_8ENCODER_ADDR)

def handle_encoder():
    global channels
    for i in range(8):
        if not encoder.read(0x50 + i)[0]:
            encoder.write(0x40 + i, [1])
    new_channels = [rect.Rect(x=channels[i].x, y=channels[i].y, width=channels[i].width,
            height=(int(encoder.read(0x0 + 4*i)[0]) & 0x1f)*(64-4)//(2*32), fill=channels[i].fill) for i in range(8)]
    for i in range(8):
        page.remove(channels[i])
        page.append(new_channels[i])
    channels = new_channels

    led_cmd = encoder.read(0x00) + encoder.read(0x04) + encoder.read(0x08)
    if encoder.read(0x60)[0]:
        for i in range(9):
            encoder.write(0x70 + 3*i, led_cmd)
    else:
        encoder.write(0x70, led_cmd)
        for i in range(1, 9):
            encoder.write(0x70 + 3*i, b'\x00\x00\x00')

angle = I2CDevice(M5STACK_8ANGLE_ADDR)

def handle_angle():
    global channels2
    new_channels = [rect.Rect(x=channels2[i].x, y=channels2[i].y, width=channels2[i].width,
            height=(int(angle.read(0x10 + i)[0]))*(64-4)//(2*255), fill=channels2[i].fill) for i in range(8)]
    for i in range(8):
        page.remove(channels2[i])
        page.append(new_channels[i])
    channels2 = new_channels
    led_cmd = angle.read(0x10) + angle.read(0x11) + angle.read(0x12) + bytes([50])
    if angle.read(0x20)[0]:
        for i in range(9):
            angle.write(0x30 + 4*i, led_cmd)
    else:
        angle.write(0x30, led_cmd)
        for i in range(1, 9):
            angle.write(0x30 + 4*i, b'\x00\x00\x00\x00')

try:
    while True:
        while not i2c.try_lock(): pass
        #devinfo = str([hex(device_address) for device_address in i2c.scan()])
        #print("I2C addresses found:", devinfo)
        try:
            handle_encoder()
            handle_angle()
        except:
            print("Failed")
        i2c.unlock()
        time.sleep(0.05)
finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
    i2c.unlock()
