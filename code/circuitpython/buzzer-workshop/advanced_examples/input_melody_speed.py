"""
Description: 
    Plays Mozart - Rondo Alla Turca on the buzzer, use the button to control the speed (see https://pages.mtu.edu/~suits/notefreqs.html and https://www.youtube.com/watch?v=aynfMtX0fiY)
Cable Connections: 
    Buzzer Vcc -> 3V3
    Buzzer Gnd -> GND
    Buzzer I/O -> D7
    Button + -> 3V3
    Button - -> GND
    Button S -> D0
"""
import board
import simpleio
import time
from digitalio import DigitalInOut, Direction

melody = [(493.88, 1.0), (440, 1.0), (415.30, 1.0), (440, 1.0), (523.25, 2.0), (-1, 2.0), (587.33, 1.0),(523.25, 1.0),(493.88, 1.0),(523.25, 1.0),(659.25, 2.0),(-1, 2.0),(698.46, 1.0),(659.25, 1.0),(622.25, 1.0),(659.25, 1.0), (987.77, 1.0),(880.00, 1.0),(830.61, 1.0),(880.00, 1.0), (987.77, 1.0),(880.00, 1.0),(830.61, 1.0),(880.00, 1.0), (1046.50, 2.0), (-1, 2.0),]

#different speed values, feel free to change these
speed = [0.3, 0.1, 0.05, 0.02]
currentSpeed = 0 % len(speed)

#change this to true for different sensors
activeState = False 

# blackout period where we are ignoring the input signal
blackout = 0.5


# Set the D0 pin up to read from the sensor
input = DigitalInOut(board.D0)
input.direction = Direction.INPUT

while True:

    for note, duration in melody:
        
        multiplier = speed[currentSpeed]
        blackout += multiplier*duration

        if note >= 0:
            simpleio.tone(board.D7, note, duration=multiplier*duration)
        else:
            time.sleep(multiplier*duration)
        
        if input.value == activeState and blackout >= 0.5:
            #wrap around array using mod (%)  
            currentSpeed = (currentSpeed+1) % len(speed)
            blackout = 0
            