from digitalio import DigitalInOut
import time


class RainbowAnimation:
    def __call__(self, robot):
        robot.rainbow.animate()


class LineFollowing:
    def __call__(self, robot):
        robot.motors.drive(robot.line_left.value, robot.line_right.value)


class DistanceBeeping:
    def __init__(self, close_distance=15):
        self.last_beep = time.monotonic()
        self.close_distance = close_distance

    def __call__(self, robot):
        d = robot.get_sonar_distance()
        print(d)
        if d is None:
            return
        now = robot.now
        # At 10 cm to "close distance" boundary we will beep
        # twice per second.
        if now - self.last_beep > (d - self.close_distance) * 0.05:
            robot.beep()
            self.last_beep = now


class ObstacleAvoidance:
    def __init__(self, close_distance=15):
        # Only act if we get at least 3 consequential "close"
        # measurements.
        self.n_close_measurements = 0
        self.close_distance = close_distance

    def __call__(self, robot):
        d = robot.get_sonar_distance()
        if d is None:
            return
        if d < self.close_distance:
            self.n_close_measurements += 1
            if self.n_close_measurements >= 2:
                robot.motors.drive(-1, 1)
                # This prevents all other behaviors
                # for a short while
                robot.sleep(0.3)
        else:
            self.n_close_measurements = 0


class IRObstacleAvoidance:
    def __init__(self, pin):
        self.pin = DigitalInOut(pin)

    def __call__(self, robot):
        if not self.pin.value:
            robot.motors.drive(-1, 1)
            # This prevents all other behaviors
            # for a short while
            robot.sleep(0.4)


class OnButtonClick:
    def __init__(self, behavior):
        self.behavior = behavior

    def __call__(self, robot):
        event = robot.keys.events.get()
        if event and event.released:
            self.behavior(robot)


class TimedSequence:
    """Cycles through a given sequence of behaviours.

    Stays at each behaviour for a given number of seconds.
    """

    def __init__(self, behaviors_with_durations):
        self.behaviors_with_durations = behaviors_with_durations
        self.last_switch_time = time.monotonic()
        self.current_behavior = 0

    def __call__(self, robot):
        behavior, duration = self.behaviors_with_durations[self.current_behavior]
        if robot.now - self.last_switch_time >= duration:
            self.current_behavior += 1
            if self.current_behavior >= len(self.behaviors_with_durations):
                self.current_behavior = 0
            self.last_switch_time = robot.now
            behavior, duration = self.behaviors_with_durations[self.current_behavior]
        behavior(robot)


class MinLoopDuration:
    """This behaviour can be added at the end of the list of behaviours.
    It will then have the robot sleep until the loop takes a fixed duration.
    """

    def __init__(self, loop_duration):
        self._loop_duration = loop_duration
        self.last_loop_work_time = None

    def __call__(self, robot):
        self.last_loop_work_time = time.monotonic() - robot.now
        robot.sleep(max(0, self._loop_duration - self.last_loop_work_time))
