import board
import busio

CMD_LEFT = 1
CMD_RIGHT = 2

class HC05Controller:
    def __init__(self):
        self.hc05 = busio.UART(board.TX, board.RX, baudrate=9600, timeout=0.1)

    def read_command(self):
        response = self.hc05.read(1)
        if response == None:
            return None
        if response in b"FBRL0STCXAP":
            return response
        else:
            rest = self.hc05.readline() or b""
            return response + rest.strip()
