"""Example for Pico. Blinks the built-in LED."""
import time
import board
import digitalio
import analogio
import pwmio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT
buzz = pwmio.PWMOut(board.D1, frequency=450, variable_frequency=True)
analog_in = analogio.AnalogIn(board.A0)


def get_voltage(pin):
    return (pin.value * 3.3) / 65536

near = False
while True:
    if get_voltage(analog_in) > 2.0:
        led.value = False
        if not near:
            near = True
            # Play tune
            for f in (440, 880):
                buzz.frequency = f
                buzz.duty_cycle = 65535 // 2  # On 50%
                time.sleep(0.1)  # On for 1/4 second
                buzz.duty_cycle = 0  # Off
                time.sleep(0.03)  # Pause between notes
        buzz.duty_cycle = 0
    else:
        led.value = True
        near = False
    time.sleep(0.1)
