"""
Description: 
    Generates a 400Hz tone on the connected buzzer by using the simpleio library 

Cable Connections: 
    Buzzer Vcc -> 3V3
    Buzzer Gnd -> GND
    Buzzer I/O -> D7

Additional Challenges:
    - Change the pitch
    - Make a sirene
    - Play a melody
"""
import board
import simpleio

while True:
    # Play a 1s tone on the buzzer with a 400Hz frequency
    simpleio.tone(board.D7, 500, duration=1)
