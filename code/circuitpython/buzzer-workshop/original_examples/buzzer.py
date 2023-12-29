import time
import board
import pwmio
from digitalio import DigitalInOut, Direction, Pull

piezo = pwmio.PWMOut(board.A3, duty_cycle=0, frequency=440, variable_frequency=True)
switch = DigitalInOut(board.D1) #Expansion Board User Button
switch.direction = Direction.INPUT
switch.pull = Pull.UP

NOTE_LENGTH = 0.1
PAUSE_LENGTH = 0.1

def play_note(f):
    piezo.frequency = f
    piezo.duty_cycle = 65535 // 2  # On 50%
    time.sleep(NOTE_LENGTH)  # On for 1/4 second
    piezo.duty_cycle = 0  # Off
    time.sleep(PAUSE_LENGTH)  # Pause between notes

def play(fs):
    for f in fs: play_note(f)

while True:
    if switch.value == 0:
        play([262, 294, 330, 349, 392, 440, 494, 523])
