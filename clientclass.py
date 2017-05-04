import socket
import sys
import time

class Client(object):

    def connectClient(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost',8000))
        print("Client connected to socket")

    def sendMessage(self,message):
        if message != 'ENDCONN':
            self.socket.send(message.encode())



    #def connectPorts(self):
        #get all ports that are currently being used in csp.txt
        #csp   = open('csp.txt', 'r')
        #ports = csp.read().splitlines()
        #for port in ports
