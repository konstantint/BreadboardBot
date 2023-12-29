"""
Descrption:
    Blinks the green onboard LED once per second.

Cable connections: 
    None

Additional Challenges: 
    - Make the LED blink 10 times per second
    - Change the code to blink the RED led
    - Build a police sirene with the blue and the red led blinking simultaneously
"""
import board
import time
from digitalio import DigitalInOut, Direction

# Setup the Green LED
led = DigitalInOut(board.LED_GREEN)
led.direction = Direction.OUTPUT

# Start endless loop
while True:
    # Turn LED on 
    led.value = True
    time.sleep(0.5)
    # Turn LED off
    led.value = False
    time.sleep(0.5)
