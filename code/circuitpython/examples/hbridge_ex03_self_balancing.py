from breadboardbot.behaviors import MinLoopDuration
from breadboardbot.platform_rp2040_hbridge import *
from breadboardbot.self_balancing import *

bot = Robot(mpu=True, line_sensors=False)

# NB: For the robot configuration described in the example
# (with raised battery box and MPU located closer to the center of mass)
# decent stability can be achieved by estimating the angle in the most naive way
# from the accelerometer data as atan3(acc_z, acc_y).
# But since we have a fancier angle estimation implementation from the Servo-motor
# example, why not use it here anyway.
mpu_processor = MPUBalancingAngleProcessor(
    bot.mpu, precalibration_wait_duration=2, calibration_duration=1, loop_period=0.005
)
self_balancing = SelfBalancing(
    # These coefficients haven't been tuned too much - a reasonably wide
    # range of values seems to work.
    DiscretePIDController(k_p=0.06, k_d=0.05, k_i=0.001),
    mpu_processor,
)

bot.loop_forever(behaviors=[mpu_processor, self_balancing, MinLoopDuration(0.005)])
