"""
Description: 
    Plays Mozart - Rondo Alla Turca on the buzzer, use the joystick to control the speed (see https://pages.mtu.edu/~suits/notefreqs.html and https://www.youtube.com/watch?v=aynfMtX0fiY)
Cable Connections: 
    Buzzer Vcc -> 3V3
    Buzzer Gnd -> GND
    Buzzer I/O -> D7
    Joystick +5W -> 3V3
    Joystick GND -> GND
    Joystick VRx -> A1
"""
import board
import simpleio
import time
from analogio import AnalogIn

melody = [(493.88, 1.0), (440, 1.0), (415.30, 1.0), (440, 1.0), (523.25, 2.0), (-1, 2.0), (587.33, 1.0),(523.25, 1.0),(493.88, 1.0),(523.25, 1.0),(659.25, 2.0),(-1, 2.0),(698.46, 1.0),(659.25, 1.0),(622.25, 1.0),(659.25, 1.0), (987.77, 1.0),(880.00, 1.0),(830.61, 1.0),(880.00, 1.0), (987.77, 1.0),(880.00, 1.0),(830.61, 1.0),(880.00, 1.0), (1046.50, 2.0), (-1, 2.0),]

analogin1 = AnalogIn(board.A1)

def get_voltage(pin):
    return ((pin.value* 1)/ 65536)*0.5 + 0.01

while True:
    for note, duration in melody:

        multiplier = get_voltage(analogin1)
        if note >= 0:
            simpleio.tone(board.D7, note, duration=multiplier*duration)
        else:
            time.sleep(multiplier*duration)