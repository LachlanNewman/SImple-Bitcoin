import socket
import sys
import threading
import ssl

class Server(object):

    def __init__(self, host, port):
        self.host = host #host name
        self.port = port #port for server

    def connectServer(self):
        self.socket = socket.socket()
        #while loop keeps socket open until client disconects
        while True:
            try:
                #test to see if the port is open
                self.socket.bind((self.host,self.port))
                #if port is open write port number to file csp.txt
                #csp = open('csp.txt', 'a+')
                #csp.write(str(self.port)+'\n')
                #csp.close()
                break
            except socket.error as e:
                if e.errno == 98:
                    print("Port is already in use")
                    #add 1 to try another port and see if it is open
                    self.port += 1
                else:
                    print(e)

        self.socket.listen(5)

    def acceptClients(self):

        def clientthread(connstream):
            #infinite loop so that function do not terminate and thread do not end.
             while True:
            #Receiving from client

                data = connstream.read()# 1024 stands for bytes of data to be received
                if not data:
                    continue
                else:
                    print("from thread:" , threading.current_thread(), data)
        #allow socket to accept connection from clients

        for i in range(5):

            self.connection, self.address = self.socket.accept()
            print("connnecetion")

            try:
                connstream = ssl.wrap_socket(self.connection,
                                                server_side=True,
                                                 certfile="mycert.pem",
                                                 keyfile="mycert.pem")
            except socket.error as e:
                print("SERVERError[" + str(e.errno) + "]: " + e.strerror)
                break

            #Creating new thread. Calling clientthread function for this function and passing conn as argument.
            client = threading.Thread(target=clientthread,args=(connstream,)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            client.start()

        self.connection.close()
        self.socket.close





    def connectClient(self):
        print("client action")
