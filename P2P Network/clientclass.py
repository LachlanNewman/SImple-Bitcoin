import socket
import sys

class Client(object):

    def connectClient(self):
        self.socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket1.connect(('localhost',8000))
        self.socket2.connect(('localhost',8001))
        self.socket3.connect(('localhost',8002))
        print("Client connected to socket ")

    def sendMessage(self,message):
        self.socket1.send(message.encode())
        self.socket2.send(message.encode())
        self.socket3.send(message.encode())
