"""
Description: 
    Generates a 400Hz tone on a connected buzzer

Cable Connections: 
    Buzzer Vcc -> 3V3
    Buzzer Gnd -> GND
    Buzzer I/O -> D7

Additional Challenges:
    - Change the pitch of the tone
    - Make a sirene that changes pitch

"""
import board
import time
from digitalio import DigitalInOut, Direction

# Setup the buzzer
buzzer = DigitalInOut(board.D7)
buzzer.direction = Direction.OUTPUT

# Start the endless loop
while True:

    # Pull the buzzer membrane up for a short amount of time
    buzzer.value = True
    time.sleep(0.001)

    # Pull the buzzer membrane down for a short amount of time
    buzzer.value = False
    time.sleep(0.001)

