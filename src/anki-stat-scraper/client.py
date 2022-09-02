import socket
import struct

class Client:
    def __init__(self):
        self.HEADER = 128
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "147.182.205.81"
        self.ADDR = (self.SERVER, self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

    def send(self, msg):
        msg = struct.pack('>I', len(msg)) + msg.encode(self.FORMAT)
        self.client.sendall(msg)
