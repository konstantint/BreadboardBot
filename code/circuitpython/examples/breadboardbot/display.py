import adafruit_displayio_ssd1306
import board
import displayio

displayio.release_displays()

class DisplayBehavior:
    def __init__(self, i2c, main_page, update_behavior = None):
        display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)
        self.display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)
        self.display.show(main_page)
        self.update_behavior = update_behavior

    def __call__(self, robot):
        if self.update_behavior:
            self.update_behavior(robot)
