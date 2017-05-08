import socket
import sys
import threading

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

        self.socket.listen(1)

    def acceptClients(self):

        def clientthread(conn):
            #infinite loop so that function do not terminate and thread do not end.
             while True:
            #Receiving from client

                data = conn.recv(1024).decode() # 1024 stands for bytes of data to be received
                if not data:
                    continue
                else:
                    print("from thread:" , threading.current_thread(), data)
        #allow socket to accept connection from clients

        for i in range(5):

            self.connection, self.address = self.socket.accept()

            #Creating new thread. Calling clientthread function for this function and passing conn as argument.
            client = threading.Thread(target=clientthread,args=(self.connection,)) #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
            client.start()

        self.connection.close()
        self.socket.close





    def connectClient(self):
        print("client action")
