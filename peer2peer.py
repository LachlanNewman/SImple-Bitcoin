import socket

class p2p(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connectServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        self.socket.listen(1)
        
