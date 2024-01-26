import board
from breadboardbot.behaviors import MinLoopDuration
from breadboardbot.hc06_controller import *
from breadboardbot.platform_rp2040 import *
from breadboardbot.self_balancing import *

bot = Robot(mpu=True, uart=True, line_sensors=False, motor_right_pin=board.D8)

mpu_processor = MPUBalancingAngleProcessor(bot.mpu)
controller = DiscretePIDController(k_p=0.03, k_d=0.015, k_i=0.0005)
self_balancing = SelfBalancing(controller, mpu_processor)
self_balancing.paused = True
loop_guard = MinLoopDuration(0.005)


def handle_command(cmd):
    global bot, self_balancing
    if cmd == b"stats\n":
        loop_time = loop_guard.last_loop_work_time
        message = f"C: {mpu_processor.calibrated_angle:.3f}, T: {mpu_processor.current_angle:.3f}, S: {self_balancing.signal}, L: {loop_guard.last_loop_work_time:.5f}"
        bot.uart.write(message.encode("ascii"))
    elif cmd == b"pause\n":
        self_balancing.paused = not self_balancing.paused
        bot.uart.write(f"Paused: {self_balancing.paused}\n".encode("ascii"))
    elif cmd == b"cal\n":
        mpu_processor.calibrate()
        bot.uart.write(b"Calibration started\n")
    elif cmd.startswith(b"p+ "):
        controller.k_p += float(cmd[3:])
        bot.uart.write(f"New Kp: {controller.k_p}\n".encode("ascii"))
    elif cmd.startswith(b"i+ "):
        controller.k_i += float(cmd[3:])
        bot.uart.write(f"New Ki: {controller.k_i}\n".encode("ascii"))
    elif cmd.startswith(b"d+ "):
        controller.k_d += float(cmd[3:])
        bot.uart.write(f"New Kd: {controller.k_d}\n".encode("ascii"))
    else:
        bot.uart.write(b"?\n")


# Print MPU angles to the Mu editor serial plotter.
print_every = IntModN(-1, 25)


def StatsPrinter(robot):
    global mpu_processor
    if print_every.next() == 0:
        print(
            f"({mpu_processor.current_angle}, {mpu_processor.raw_acc_angle}, {mpu_processor.acc_angle}, {mpu_processor.calibrated_angle})"
        )


bot.loop_forever(
    behaviors=[
        mpu_processor,
        self_balancing,
        HC06Listener(bot.uart, handle_command, readline=True),
        # StatsPrinter,
        loop_guard,
    ]
)
