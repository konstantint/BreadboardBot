class HC06Listener:
    def __init__(self, uart, command_handler, readline=False):
        self._uart = uart
        self._command_handler = command_handler
        self._readline = readline

    def __call__(self, robot):
        while self._uart.in_waiting:
            cmd = self._uart.readline() if self._readline else self._uart.read(1)
            self._command_handler(cmd)
