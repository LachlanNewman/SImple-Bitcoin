import socket
import sys

class Client(object):

    def connectClient(self):
        self.sockets = {}
        print(self.ports)
        for port in self.ports:
            self.sockets['socket_'+ port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sockets['socket_'+ port].connect(('localhost',int(port)))
        print("Client connected to socket ")

    def sendMessage(self,message):
        for port in self.ports:
            self.sockets['socket_' + port].send(message.encode())

    def getPortsUsed(self):
        csp = open('csp.txt', 'r')
        self.ports = csp.read().splitlines()
        csp.close()
