import board
import busio
import displayio
import terminalio
import adafruit_displayio_ssd1306
from adafruit_display_text import label
from adafruit_display_shapes import  circle
import  time

# Devices
displayio.release_displays()
i2c = busio.I2C (scl=board.SCL, sda=board.SDA)
display_bus = displayio.I2CDisplay (i2c, device_address = 0x3C) # The address of my Board
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64)

c = circle.Circle(x0=70, y0=20, r=10, fill=0, outline=0xFFFFFF)
dx = dy = 1

def make_page():
    page = displayio.Group() # no max_size needed
    color_bitmap = displayio.Bitmap(128, 64, 1) # Full screen white
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF  # White

    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    page.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(118, 54, 1)
    inner_palette = displayio.Palette(1)
    inner_palette[0] = 0x000000  # Black
    inner_sprite = displayio.TileGrid(inner_bitmap, pixel_shader=inner_palette, x=5, y=4)
    page.append(inner_sprite)
     
    # Draw a label
    text = "Hello"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=28, y=15)
    page.append(text_area)

    text = "World"
    text_area = label.Label(terminalio.FONT, text=text, color=0xFFFF00, x=32, y=25)
    page.append(text_area)
    
    page.append(c)
    return  page

display.show(make_page())

while True:
    time.sleep(0.01)
    c.x0 += dx
    if c.x0 > 128 - c.r or c.x0 < c.r:
        dx = -dx
        c.x0 += 2*dx
        
    c.y0 += dy
    if c.y0 > 64 - c.r or c.y0 < c.r:
        dy = -dy
        c.y0 += 2*dy
