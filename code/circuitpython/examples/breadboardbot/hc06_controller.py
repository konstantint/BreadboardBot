class HC06Listener:
    def __init__(self, uart, command_handler):
        self.uart = uart
        self.command_handler = command_handler

    def __call__(self, robot):
        while self.uart.in_waiting:
            self.command_handler(self.uart.read(1))
