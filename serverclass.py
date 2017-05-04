import socket
import sys

class Server(object):

    def __init__(self, host, port):
        self.host = host #host name
        self.port = port #port for server

    def connectServer(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #while loop keeps socket open until client disconects
        while True:
            try:
                #test to see if the port is open
                self.socket.bind((self.host,self.port))
                #if port is open write port number to file csp.txt
                #csp = open('csp.txt', 'a+')
                #csp.write(str(self.port)+',')
                #csp.close()
                break
            except socket.error as e:
                if e.errno == 98:
                    print("Port is already in use")
                    #add 1 to try another port and see if it is open
                    self.port += 1
                else:
                    print(e)

        self.socket.listen(1)

    def acceptClients(self):
        #allow socket to accept connection from clients
        self.connection, self.address = self.socket.accept()
        #while loop keeps sockets open until clients leave
        while True:
            data = self.connection.recv(1024).decode()
            if not data:
                break
            print ("from connected  user: " + str(data))

        self.connection.close()

    def connectClient(self):
        print("client action")
