# Classic PID-based self-balancing

import adafruit_mpu6050
from collections import deque
import math
import time


class IntModN:
    """Represents an integer modulo N.
    Useful as a counter to do something every Nth time.
    """

    def __init__(self, value, n):
        self._n = n
        self._value = value % n

    def next(self):
        self._value = (self._value + 1) % self._n
        return self._value


class LowPassFilter:
    def __init__(self, alpha, initial_value=None):
        self._alpha = alpha
        self._current_value = initial_value

    def set(self, new_value):
        self._current_value = new_value

    def __call__(self, new_value):
        if self._current_value is None:
            self._current_value = new_value
        else:
            self._current_value = (
                self._alpha * self._current_value + (1 - self._alpha) * new_value
            )
        return self._current_value


class MPUBalancingAngleProcessor:
    """A processor for the MPU signal that deals with calibration and balance angle estimation.

    Note that if the robot is reasonably slow and the MPU is positioned either close to the center of mass
    or high enough, where it does not get jerked around too much, you can read out the
    balancing angle by just doing atan2(acc_z, acc_x) and this will be good enough to stabilize it.

    Unfortunately, the MCU plugged into the BreadboardBot is located at a place that picks up even
    the slightest accelerations from the wheels. As a result, accelerometer provides a very noisy balancing
    signal, and it is hard enough to balance the BreadboardBot already.

    The gyro provides a much cleaner angular signal instead, however it needs to be calibrated
    and kept from drifting.

    This class deals with the calibration behavior for the gyro and the "balance angle"
    as well as with the readout of the reasonably clean angle signal.
    """

    def __init__(
        self,
        mpu,
        # Time in seconds we just wait doing nothing after calibrate() is called.
        # This gives the user some time to position the robot.
        precalibration_wait_duration=2,
        # Time in seconds we collect calibration data.
        calibration_duration=1,
        # This assumes we maintain a fixed loop duration.
        loop_period=0.005,
    ):
        self._mpu = mpu
        self._precalibration_wait_duration = precalibration_wait_duration
        self._max_calibration_points = int(calibration_duration / loop_period)
        self._loop_period = loop_period
        # We will read the gyro every loop, but the accelerometer every 10 steps
        # Otherwise we can't fit into the 0.005 loop duration.
        self._acc_counter = IntModN(-1, 10)
        mpu.gyro_range = adafruit_mpu6050.GyroRange.RANGE_1000_DPS
        self.calibrate()

    def calibrate(self):
        self._calibration_start_time = time.monotonic()
        self._calibrated_acc_angle_sum = 0
        self._calibrated_gyro_d_angle_sum = 0
        self._calibrated_acc_angle = 0
        self._calibrated_gyro_d_angle = 0
        self._n_calibration_points = 0
        # We read the angle from the accelerometer with a lot of smoothing,
        # because we do not care about any jerky movements, only the gravity.
        self._acc_angle_smoother = LowPassFilter(0.9)
        self._current_angle = 0
        # These are kept as fields to allow print debugging
        self.raw_acc_angle = 0
        self.acc_angle = 0
        self.gyro_angle = 0
        self.gyro_d_angle = 0

    @property
    def calibrated_angle(self):
        return self._calibrated_acc_angle

    @property
    def current_angle(self):
        return self._current_angle

    @property
    def is_calibrating(self):
        return self._n_calibration_points <= self._max_calibration_points

    def get_raw_acc_angle(self):
        """Returns the raw "balancing" angle in degrees by reading the MPU.

        Returns value around 90 = Face down, 0 = Up, -90 = Face up,
        if the MPU is plugged into the Breadboard as shown in the example docs.
        """
        acc_x, acc_y, acc_z = self._mpu.acceleration
        return math.atan2(acc_z, acc_x) * 180 / math.pi

    def get_raw_gyro_d_angle(self):
        """Returns the raw angular (deg/s) around the balancing axis."""
        gyr_x, gyr_y, gyr_z = self._mpu.gyro
        return gyr_y * 180 / math.pi

    def __call__(self, robot):
        if self._n_calibration_points > self._max_calibration_points:
            # Read and filter values appropriately
            if self._acc_counter.next() == 0:
                self.raw_acc_angle = self.get_raw_acc_angle()
                self.acc_angle = self._acc_angle_smoother(self.raw_acc_angle)
            self.gyro_d_angle = (
                self.get_raw_gyro_d_angle() - self._calibrated_gyro_d_angle
            )
            self.gyro_angle = (
                self._current_angle + self._loop_period * self.gyro_d_angle
            )
            # We only read the accelerometer to counteract any gyro drift.
            self._current_angle = 0.999 * self.gyro_angle + 0.001 * self.acc_angle
        elif (
            robot.now - self._calibration_start_time
            < self._precalibration_wait_duration
        ):
            pass  # Just wait
        elif self._n_calibration_points < self._max_calibration_points:
            # Collect calibration data
            self._n_calibration_points += 1
            self._calibrated_acc_angle_sum += self.get_raw_acc_angle()
            self._calibrated_gyro_d_angle_sum += self.get_raw_gyro_d_angle()
            robot.led_blue.value = bool((self._n_calibration_points // 20) % 2)
        else:
            # Calibration completed (self._n_calibration_points == self._max_calibration_points)
            self._calibrated_acc_angle = (
                self._calibrated_acc_angle_sum / self._n_calibration_points
            )
            self._calibrated_gyro_d_angle = (
                self._calibrated_gyro_d_angle_sum / self._n_calibration_points
            )
            self._acc_angle_smoother.set(self._calibrated_acc_angle)
            self._current_angle = self._calibrated_acc_angle
            self._n_calibration_points += 1


class DifferenceFilter:
    def __init__(self, initial_value=None):
        self._last_value = initial_value

    def __call__(self, new_value):
        if self._last_value is None:
            result = 0
        else:
            result = new_value - self._last_value
        self._last_value = new_value
        return result


class DiscretePIDController:
    def __init__(self, k_p, k_i, k_d, sum_err_cap=100):
        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d
        self._err_differencer = DifferenceFilter()
        self._sum_err = 0
        self._sum_err_cap = sum_err_cap

    def __call__(self, observed, target):
        err = observed - target
        d_err = self._err_differencer(err)
        self._sum_err = max(
            -self._sum_err_cap, min(self._sum_err + err, self._sum_err_cap)
        )
        return self.k_p * err + self.k_d * d_err + self.k_i * self._sum_err


class SelfBalancing:
    def __init__(self, controller, mpu_processor):
        self._controller = controller
        self._mpu_processor = mpu_processor
        self.paused = False
        # For debugging
        self.signal = 0

    def __call__(self, robot):
        self.signal = self._controller(
            self._mpu_processor.current_angle, self._mpu_processor.calibrated_angle
        )
        if self.paused or self._mpu_processor.is_calibrating:
            robot.motors.drive(0, 0)
        else:
            robot.motors.drive(self.signal, self.signal)
