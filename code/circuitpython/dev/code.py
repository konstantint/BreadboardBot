import adafruit_dht
import adafruit_displayio_ssd1306
import board
from digitalio import DigitalInOut, Direction, Pull
import displayio
import random
import time
import face

displayio.release_displays()
display_bus = displayio.I2CDisplay(board.I2C(), device_address=0x3c)
display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=128, height=64, rotation=180)

face = face.Face()
display.show(face)
eye_cycle = 0

dht = adafruit_dht.DHT11(board.D10)

while True:
    face.say("Temp: " + str(dht.temperature) + "C  Hum: " + str(dht.humidity) + "%")
    eye_cycle = (eye_cycle + 1) % 4
    face.look(0 if (eye_cycle % 2) == 0 else eye_cycle - 2)
    time.sleep(1)
