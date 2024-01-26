from adafruit_motor import motor, servo
import pwmio


class MotorsModel:
    FS90R = 1
    GEEKSERVO = 2


class ContinuousServoMotors:
    """Continuous servo motors abstraction."""

    def __init__(self, left_pin, right_pin, motors_model=MotorsModel.FS90R):
        if motors_model == MotorsModel.FS90R:
            min_pulse, max_pulse = 700, 2300
            self.speed_multiplier = 0.2
            self.speed_multiplier = 1.0
        else:
            min_pulse, max_pulse = 500, 2500
            self.speed_multiplier = 0.5
        self.left = servo.ContinuousServo(
            pwmio.PWMOut(left_pin, frequency=200),
            min_pulse=min_pulse,
            max_pulse=max_pulse,
        )
        self.right = servo.ContinuousServo(
            pwmio.PWMOut(right_pin, frequency=200),
            min_pulse=min_pulse,
            max_pulse=max_pulse,
        )

    def drive(self, left_throttle, right_throttle):
        # Every cheap servo is a unique snowflake and if you want to get
        # better precision, you might want to calibrate the constants used
        # here until calling drive(0, 0) consistently results in fully stopped
        # motors
        # -0.1 .. -0.03 -> zero throttle at ~ -0.075,
        # about +-0.03 around it no movement
        self.left.throttle = min(
            1, max(self.speed_multiplier * left_throttle - 0.06, -1)
        )
        # -0.01 .. 0.05 -> zero throttle at ~0.02, about +-0.03 
        self.right.throttle = min(
            1, max(-1 * (self.speed_multiplier * right_throttle - 0.01), -1)
        )


class HBridgeDCMotors:
    """DC motors connected over an H-Bridge driver."""

    def __init__(self, left_back_pin, left_fwd_pin, right_back_pin, right_fwd_pin):
        self.left = motor.DCMotor(
            pwmio.PWMOut(left_back_pin, frequency=50),
            pwmio.PWMOut(left_fwd_pin, frequency=50),
        )
        self.right = motor.DCMotor(
            pwmio.PWMOut(right_back_pin, frequency=50),
            pwmio.PWMOut(right_fwd_pin, frequency=50),
        )

    def drive(self, left_throttle, right_throttle):
        self.left.throttle = min(1, max(left_throttle, -1))
        self.right.throttle = min(1, max(right_throttle, -1))
