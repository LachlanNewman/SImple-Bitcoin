import socket

class p2p(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connectServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        self.socket.listen(1)

    def acceptClients(self):
        self.connection, self.address = self.socket.accept()
        while True:
            data = self.connection.recv(1024).decode()
            if not data:
                break
            print ("from connected  user: " + str(data))

            data = input("->")
            print ("sending: " + str(data))
            self.connection.send(data.encode())

        self.connection.close()
