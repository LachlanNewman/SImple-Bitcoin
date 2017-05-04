import socket

class p2p(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connectServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.socket.bind((self.host,self.port))
                print('port', self.port , 'available' )
                break
            except socket.error as e:
                if e.errno == 98:
                    print("Port is already in use")
                    self.port += 1
                else:
                    print(e)

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
