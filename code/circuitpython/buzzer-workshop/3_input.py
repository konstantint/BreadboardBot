"""
Description: 
    Plays a tone on the buzzer when the button is pressed.

Cable Connections: 
    Buzzer Vcc -> 3V3
    Buzzer Gnd -> GND
    Buzzer I/O -> D7

    Button -> D9
    Button -> GND

Additional Challenges:
    - Play a melody when the button is pressed
    - Replace the button with a sensor
    - Use multiple sensors and do different actions for each of them
"""
import board
import simpleio
from digitalio import DigitalInOut, Direction, Pull
import time

# Set the D9 pin up to read from the sensor / button
input = DigitalInOut(board.D9)
input.direction = Direction.INPUT
input.pull = Pull.UP

while True:
    # If the sensor is activated, play a short tone on the buzzer
    if input.value == False:
        simpleio.tone(board.D7, 400, duration=0.3)
    time.sleep(0.1)
