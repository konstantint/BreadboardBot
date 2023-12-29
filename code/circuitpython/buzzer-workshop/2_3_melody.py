"""
Description: 
    Plays a simple melody on the connected buzzer

Cable Connections: 
    Buzzer Vcc -> 3V3
    Buzzer Gnd -> GND
    Buzzer I/O -> D7

Additional Challenges:
    - Change the code to play notes at different lengths
    - Play a melody you know (Star wars, Whilhelm Tell, ...)
"""
import board
import simpleio
import time

# Defines the melody to be played. Each entry in the list is a note that is played for 0.3 seconds
melody = [400, 800, 400, 800]
while True:
    # Play each note in the melody
    for note in melody:
        simpleio.tone(board.D7, note, duration=0.3)

    # Wait for a bit before playing the melody again 
    time.sleep(1.0)
