"""
Description:
    Plays Wilhelm Tell - (see https://pages.mtu.edu/~suits/notefreqs.html and https://www.youtube.com/watch?v=aynfMtX0fiY)
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

melody = [
        (261.63, 0.5),
        (261.63, 0.5),
        (261.63, 1.0),
        (261.63, 0.5),
        (261.63, 0.5),
        (261.63, 1.0),
        (261.63, 0.5),
        (261.63, 0.5),
        (349.23, 1.0),
        (392.00, 1.0),
        (440.00, 1.0),
        (261.63, 0.5),
        (261.63, 0.5),
        (261.63, 1.0),
        (261.63, 0.5),
        (261.63, 0.5),
        (349.23, 1.0),
        (440.00, 1.0),
        (392.00, 1.0),
        (329.63, 1.0),
        (261.63, 1.0),
        (261.63, 0.5),
        (261.63, 0.5),
        (261.63, 1.0),
        (261.63, 0.5),
        (261.63, 0.5),
        (261.63, 1.0),
        (261.63, 0.5),
        (261.63, 0.5),
        (349.23, 1.0),
        (392.00, 1.0),
        (440.00, 1.0),
        (349.23, 0.5),
        (440.00, 0.5),
        (523.25, 2.5),
        (466.16, 0.5),
        (440.00, 0.5),
        (392.00, 0.5),
        (349.23, 1.0),
        (440.00, 1.0),
        (349.23, 1.0),

]

analogin1 = AnalogIn(board.A1)


def get_voltage(pin):
    return ((pin.value * 1) / 65536) * 0.5 + 0.01


while True:
    for note, duration in melody:

        multiplier = get_voltage(analogin1)
        if note >= 0:
            simpleio.tone(board.D7, note, duration=multiplier * duration)
        else:
            time.sleep(multiplier * duration)
